import sys
from os import path
from io import StringIO
from pytest import fixture

sys.path.append(path.abspath(path.join(path.dirname(__file__),
                path.pardir)))

from encryptoenv.CLI import CLI
from encryptoenv.FileObject import FileObject


@fixture
def base_args(tmp_path):
    env_dir_path = path.join(str(tmp_path), 'env')
    return [
        "my_key.pem",
        "-v",
        "-e",
        env_dir_path
    ]


@fixture
def base_args_with_vars(base_args):
    print("BASE ARGS", id(base_args))
    new_args_list = base_args[:]
    new_args_list.append("-a 'test=123' 'test1=123'")
    return new_args_list


@fixture
def base_args_with_vars_encrypted(base_args_with_vars):
    print("BASE ARGS WITH VARS", id(base_args_with_vars))
    new_args_list = base_args_with_vars[:]
    new_args_list.append('-E')
    return new_args_list


@fixture
def base_args_decrypted(base_args):
    new_args_list = base_args[:]
    new_args_list.append('-D')
    return new_args_list


def test_environment_path(base_args):
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    my_cli = CLI(base_args)
    my_cli.run_script()
    sys.stdout = old_stdout
    stdout_value = mystdout.getvalue()
    env_path = """'environment_path': """ + "'" + base_args[3] + "'"
    assert """'pem_filename': 'my_key.pem'""" in stdout_value
    assert env_path in stdout_value
    assert path.exists(path.join(base_args[3], base_args[0]))


def test_blank_file(base_args):
    base_args.append('-b')
    my_cli = CLI(base_args)
    my_cli.run_script()
    env_file = FileObject(path.join(base_args[3], '.env'))
    assert env_file.filepath_exists()
    assert env_file.is_empty()


def test_append_variables(base_args_with_vars):
    my_cli = CLI(base_args_with_vars)
    my_cli.run_script()
    env_file = FileObject(path.join(base_args_with_vars[3], '.env'))
    assert env_file.filepath_exists()
    assert not env_file.is_empty()


def test_encrypt_and_decrypt(
        base_args_with_vars_encrypted, base_args_decrypted):
    print("BASE ARGS WITH VARS ENCRYPTED", id(base_args_with_vars_encrypted))
    print("******************", base_args_with_vars_encrypted)
    my_cli = CLI(base_args_with_vars_encrypted)
    my_cli.run_script()
    env_file = FileObject(
        path.join(base_args_with_vars_encrypted[3], '.env'))
    assert env_file.is_binary()
    assert env_file.filepath_exists()
    assert not env_file.is_empty()
    my_cli = CLI(base_args_decrypted)
    my_cli.run_script()
    assert not env_file.is_binary()
    assert not env_file.is_empty()
    print(env_file.get_contents_of_file())


def test_clear_option(base_args):
    base_args.append('--clear')
    my_cli = CLI(base_args)
    my_cli.run_script()

    # create fixture with variables already attached
    # test that --clear works with binary
    # test that blank doesn't clear file that already exists
    # test -name

@fixture
def file_object(tmp_path):
    my_file = FileObject(path.join(tmp_path, 'env'))
    return my_file


def test_file_object_create_and_delete_filepath(file_object):
    assert not file_object.filepath_exists()
    file_object.create_filepath()
    assert file_object.filepath_exists()
    file_object.delete_file()
    assert not file_object.filepath_exists()


def test_file_object_str(file_object):
    assert file_object.get_filepath() == str(file_object)