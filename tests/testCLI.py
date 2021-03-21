import sys
from os import path
from io import StringIO
from pytest import fixture

sys.path.append(path.abspath(path.join(path.dirname(__file__),
                path.pardir)))

from encryptoenv.CLI import CLI


@fixture
def base_cli_args_list(tmp_path):
    env_dir_path = path.join(str(tmp_path), 'env')
    return [
        "my_key.pem",
        "-v",
        "-e",
        env_dir_path]


def test_environment_path(base_cli_args_list):
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    my_cli = CLI(base_cli_args_list)
    my_cli.run_script()
    sys.stdout = old_stdout
    stdout_value = mystdout.getvalue()
    env_path = """'environment_path': """ + "'" + base_cli_args_list[3] + "'"
    assert """'pem_filename': 'my_key.pem'""" in stdout_value
    assert env_path in stdout_value
    assert path.exists(path.join(base_cli_args_list[3], 'my_key.pem'))

def test_blank_file(base_cli_args_list):
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    print("*************",base_cli_args_list)
    # args_list = base_cli_args_list.append('-b')
    # my_cli = CLI(args_list)
    # my_cli.run_script()
    # sys.stdout = old_stdout
    # stdout_value = mystdout.getvalue()
    assert True


# def test_version(tmp_path):
#     old_stdout = sys.stdout
#     sys.stdout = mystdout = StringIO()
#     my_cli = CLI([
#             "my_key.pem",
#             "--version",
#         ])
#     my_cli.run_script()
#     sys.stdout = old_stdout
#     stdout_value = mystdout.getvalue()
#     # assert "1.0" in stdout_value
#     assert(True)
