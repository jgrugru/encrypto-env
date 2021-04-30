import sys
from os import path, listdir, environ
from io import StringIO                     # noqa: F401
from pytest import fixture, fail

sys.path.append(path.abspath(path.join(path.dirname(__file__),
                path.pardir)))

from encryptoenv.CLI import CLI             # noqa: E402
from encryptoenv.EnvFile import EnvFile     # noqa: E402


@fixture
def environment_path(tmp_path):
    return path.join(str(tmp_path), 'env/')


@fixture
def base_args(environment_path):
    env_dir_path = environment_path
    return [
        "-v",
        "--environment-path",
        env_dir_path
    ]


@fixture
def base_args_with_vars(base_args):
    new_args_list = base_args[:]
    new_args_list.append('-a')
    new_args_list.append('test=123')
    new_args_list.append('test1=123')
    return new_args_list


@fixture
def base_args_with_vars_encrypted(base_args_with_vars):
    new_args_list = base_args_with_vars[:]
    new_args_list.append('-E')
    return new_args_list


@fixture
def base_args_decrypted(base_args):
    new_args_list = base_args[:]
    new_args_list.append('-D')
    return new_args_list


def is_there_a_pem_file(file_list):
    is_there_a_my_key_pem = False

    for file in file_list:
        if file == 'my_key.pem':
            is_there_a_my_key_pem = True

    return is_there_a_my_key_pem


def test_environment_path(base_args):
    my_cli = CLI(base_args)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    assert env_file.filepath_exists()
    assert env_file.environment_path.is_dir()


def test_append_variables(base_args_with_vars):
    my_cli = CLI(base_args_with_vars)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    assert env_file.filepath_exists()
    assert not env_file.is_empty()


def test_append_variables_on_encrypted_file(base_args_with_vars_encrypted):
    my_cli = CLI(base_args_with_vars_encrypted)
    my_cli.run_script()
    base_args_with_vars_encrypted.append('-a')
    base_args_with_vars_encrypted.append('test3=123415')
    my_cli = CLI(base_args_with_vars_encrypted)
    my_cli.run_script()
    assert 'test3=123415' and 'test1=123' and 'test=123' \
        in my_cli.get_env_file().get_decrypted_lines_as_list()


def test_clear_option(base_args, base_args_with_vars):
    my_cli = CLI(base_args_with_vars)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    assert not env_file.is_empty()
    base_args.append('--clear')
    my_cli = CLI(base_args)
    my_cli.run_script()
    assert env_file.is_empty()


def test_clear_option_on_binary(base_args, base_args_with_vars_encrypted):
    my_cli = CLI(base_args_with_vars_encrypted)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    assert not env_file.is_empty()
    base_args.append('--clear')
    my_cli = CLI(base_args)
    my_cli.run_script()
    assert env_file.is_empty()


def test_dot_env_file_option(base_args):
    base_args.append('--dot-env-file')
    base_args.append('ENV')
    my_cli = CLI(base_args)
    my_cli.run_script()
    assert my_cli.get_env_file().filepath_exists()


def test_no_key_option(base_args):
    base_args.append('--no-key')
    my_cli = CLI(base_args)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    is_there_a_pem = False
    for file in listdir(path.dirname(env_file.get_filepath())):
        if file == 'my_key.pem':
            is_there_a_pem = True
    assert not is_there_a_pem


def test_no_key_option_with_adding_variables(base_args_with_vars):
    base_args_with_vars.append('--no-key')
    my_cli = CLI(base_args_with_vars)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    file_list = listdir(path.dirname(env_file.get_filepath()))
    assert not is_there_a_pem_file(file_list)


def test_list_variables_option_with_encryption(
        base_args, base_args_with_vars_encrypted):
    my_cli = CLI(base_args_with_vars_encrypted)
    my_cli.run_script()
    base_args.append('-l')
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    my_cli = CLI(base_args)
    my_cli.run_script()
    sys.stdout = old_stdout
    stdout_value = mystdout.getvalue()
    assert 'test' and 'test1' in stdout_value


def test_list_variables_option_without_encryption(
        base_args, base_args_with_vars):
    my_cli = CLI(base_args_with_vars)
    my_cli.run_script()
    base_args.append('-l')
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    my_cli = CLI(base_args)
    my_cli.run_script()
    sys.stdout = old_stdout
    stdout_value = mystdout.getvalue()
    assert 'test' and 'test1' in stdout_value


# def test_encrypt_and_decrypt(base_args_with_vars_encrypted,
#                              base_args_decrypted):
#     my_cli = CLI(base_args_with_vars_encrypted)
#     my_cli.run_script()
#     env_file = my_cli.get_env_file()
#     contents_of_env_file = env_file.get_decrypted_data()
#     assert env_file.is_binary()
#     assert env_file.filepath_exists()
#     assert not env_file.is_empty()
#     my_cli = CLI(base_args_decrypted)
#     my_cli.run_script()
#     assert not env_file.is_binary()
#     assert contents_of_env_file == env_file.get_contents_of_file()


# def test_create_environment_variables(base_args_with_vars_encrypted):
#     my_cli = CLI(base_args_with_vars_encrypted)
#     my_cli.run_script()
#     my_env_file = my_cli.get_env_file()
#     new_env_file = EnvFile(
#         environment_path=str(my_env_file.get_environment_path()))
#     new_env_file.create_environment_variables()

#     assert environ["test"] == '123'
#     assert environ["test1"] == '123'


def test_override_of_env_file(environment_path):
    env_file1 = EnvFile(environment_path=environment_path)
    env_file1.append_text_to_file("USERNAME=jgrugru")
    assert not env_file1.is_empty()
    env_file2 = EnvFile(environment_path=environment_path)
    assert not env_file2.is_empty()


def test_override_of_rsa_key(environment_path):
    env_file1 = EnvFile(environment_path=environment_path)
    rsa_key_contents = env_file1.rsa_file.get_contents_of_file()
    env_file2 = EnvFile(environment_path=environment_path)
    assert rsa_key_contents == env_file2.rsa_file.get_contents_of_file()


def test_file_without_ending_slash(tmp_path):
    environment_path = path.join(str(tmp_path), 'env')
    env_file = EnvFile(environment_path=environment_path)
    assert env_file.get_environment_path().is_dir()


def test_plaintext_is_too_long_error(base_args):
    base_args.append('-a')
    my_string = "Lorem Ipsum is simply dummy text of \
    the printing and typesetting industry. Lorem Ipsum has \
    been the industry's standard dummy text ever since the \
    1500s, when an unknown printer took a galley of type \
    and scrambled if I was I big b"
    print("*****************************************", len(my_string))
    base_args.append(my_string)

    base_args.append('-E')
    my_cli = CLI(base_args)
    try:
        my_cli.run_script()
    except ValueError:
        fail("Plaintext is too long")
