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
    env_dir_path = path.join(str(tmp_path), 'env')
    return [
        # "-p",
        # "my_key.pem",
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
    # create a new list with a new spot in memory
    new_args_list = base_args_with_vars[:]
    new_args_list.append('-E')
    return new_args_list


@fixture
def base_args_decrypted(base_args):
    new_args_list = base_args[:]
    new_args_list.append('-D')
    return new_args_list


def test_environment_path(base_args):
    # old_stdout = sys.stdout
    # sys.stdout = mystdout = StringIO()
    my_cli = CLI(base_args)
    my_cli.run_script()
    # sys.stdout = old_stdout
    # stdout_value = mystdout.getvalue()
    # env_path = "'environment_path': " \
    #     + "'" + my_cli.get_environment_path() + "'"
    # assert "'pem_file': 'my_key.pem'" in stdout_value
    # assert env_path in stdout_value
    assert my_cli.get_pem_file().is_file()
    assert my_cli.get_environment_path().is_dir()


def test_blank_file(base_args):
    base_args.append('-b')
    my_cli = CLI(base_args)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    assert env_file.filepath_exists()
    assert env_file.is_empty()


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


def test_append_variables(base_args_with_vars):
    my_cli = CLI(base_args_with_vars)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    assert env_file.filepath_exists()
    assert not env_file.is_empty()


def test_encrypt_and_decrypt(
        base_args_with_vars_encrypted, base_args_decrypted):
    my_cli = CLI(base_args_with_vars_encrypted)
    my_cli.run_script()
    env_file = my_cli.get_env_file()
    assert env_file.is_binary()
    assert env_file.filepath_exists()
    assert not env_file.is_empty()
    # my_cli = CLI(base_args_decrypted)
    # my_cli.run_script()
    # assert not env_file.is_binary()
    # assert not env_file.is_empty()


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
    assert env_file.is_binary()
    base_args.append('--clear')
    my_cli = CLI(base_args)
    my_cli.run_script()
    assert not env_file.is_binary()
    assert env_file.is_empty()


def test_no_key_option(base_args):
    base_args.append("--no-key")
    my_cli = CLI(base_args)
    my_cli.run_script()
    assert not my_cli.get_pem_file().filepath_exists()


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
def test_file_object_create_and_delete_filepath(env_setup_for_file_object,
                                                file_path,
                                                expected_result,
                                                is_file):
    my_file = FileObject(file_path)
    my_file.create_filepath()
    assert my_file.filepath_exists() == expected_result
    assert path.isfile(my_file.get_filepath()) == is_file
    my_file.delete_file()
    assert my_file.filepath_exists() != is_file


def test_file_object_str(file_object):
    assert file_object.get_filepath() == str(file_object)


def test_file_object_get_contents_of_text_file(file_object_with_content):
    assert file_object_with_content.get_contents_of_file() == '0123456789'


def test_file_object_clear_file(file_object, file_object_with_content):
    file_object_with_content.clear_file()
    assert file_object_with_content.is_empty()
    file_object.clear_file()
    assert file_object.is_empty()
