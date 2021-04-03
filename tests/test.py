import sys
from os import path, chdir
from io import StringIO
from pytest import fixture, mark

sys.path.append(path.abspath(path.join(path.dirname(__file__),
                path.pardir)))

from encryptoenv.CLI import CLI
from encryptoenv.FileObject import FileObject


@fixture
def base_args(tmp_path):
    env_dir_path = path.join(str(tmp_path), 'env/')
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


def test_pem_file_option(base_args):
    base_args.append('-p')
    base_args.append('RSA_KEY.pem')
    my_cli = CLI(base_args)
    my_cli.run_script()
    assert my_cli.get_pem_file().filepath_exists()


def test_environment_path(base_args):
    my_cli = CLI(base_args)
    my_cli.run_script()
    assert my_cli.get_pem_file().is_file()
    assert my_cli.get_environment_path().is_dir()


def test_blank_file(base_args):
    base_args.append('-b')
    my_cli = CLI(base_args)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    assert env_file.filepath_exists()
    assert env_file.is_empty()


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
        in my_cli.get_env_file().decrypt_data_from_env_file()


def test_clear_option(base_args, base_args_with_vars):
    my_cli = CLI(base_args_with_vars)
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


def test_list_variables_option(base_args_with_vars_encrypted):
    base_args_with_vars_encrypted.append('-l')
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    my_cli = CLI(base_args_with_vars_encrypted)
    my_cli.run_script()
    sys.stdout = old_stdout
    stdout_value = mystdout.getvalue()
    assert 'test' and 'test1' in stdout_value


def test_no_key_option(base_args):
    base_args.append("--no-key")
    my_cli = CLI(base_args)
    my_cli.run_script()
    assert not my_cli.get_pem_file().filepath_exists()


def test_encrypt(base_args_with_vars_encrypted):
    my_cli = CLI(base_args_with_vars_encrypted)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    assert env_file.is_binary()
    assert env_file.filepath_exists()
    assert not env_file.is_empty()


def test_blank_option_with_already_populated_env_file(
        base_args, base_args_with_vars):
    my_cli = CLI(base_args_with_vars)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    assert not env_file.is_empty()
    base_args.append('-b')
    my_cli = CLI(base_args)
    my_cli.run_script()
    assert not env_file.is_empty()


def test_clear_option_on_binary(base_args, base_args_with_vars_encrypted):
    my_cli = CLI(base_args_with_vars_encrypted)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    assert env_file.is_binary()
    base_args.append('--clear')
    my_cli = CLI(base_args)
    my_cli.run_script()
    assert not env_file.is_binary()
    assert env_file.is_empty()

# ===================
# TESTING FILE OBJECT
# ===================


@fixture
def file_object(tmp_path):
    my_file = FileObject(path.join(tmp_path, 'env', '.env'))
    my_file.create_filepath()
    return my_file


@fixture
def file_object_with_content(file_object):
    file_object.append_data_to_file("0123456789")
    return file_object


@fixture
def env_setup_for_file_object(tmp_path):
    chdir(tmp_path)


@mark.parametrize("file_path, expected_result, is_file", [
    ("env_path/.env", True, True),
    ("./env_path/env", True, True),
    (".env_path/env", True, True),
    ("env_path/env/", True, False),
    (".env_path/env/", True, False),
    ("././././env/", True, False),
    ("././././env", True, True),
    ("../env_path/.env", True, True),
    ("../env_path1/.env/", True, False),
])
def test_fo_create_and_delete_filepath(env_setup_for_file_object,
                                       file_path,
                                       expected_result,
                                       is_file):
    my_file = FileObject(file_path)
    my_file.create_filepath()
    assert my_file.filepath_exists() == expected_result
    assert path.isfile(my_file.get_filepath()) == is_file
    my_file.delete_file()
    assert my_file.filepath_exists() != is_file


def test_fo_get_contents_of_text_file(file_object_with_content):
    assert file_object_with_content.get_contents_of_file() == '0123456789'


def test_fo_get_contents_of_binary_file(base_args_with_vars_encrypted):
    pass


def test_fo_write_data_to_text():
    pass


def test_fo_write_data_to_binary():
    pass


def test_fo_clear_file(file_object, file_object_with_content):
    file_object_with_content.clear_file()
    assert file_object_with_content.is_empty()
    file_object.clear_file()
    assert file_object.is_empty()


def test_fo_str(file_object):
    assert file_object.get_filepath() == str(file_object)
