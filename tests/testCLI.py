import sys
import os.path
from io import StringIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             os.path.pardir)))

from encryptoenv.CLI import CLI


def test_parser(tmp_path):
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    my_cli = CLI([
        "my_key.pem",
        "-v",
        "-e",
        os.path.join(tmp_path, 'env')])
    my_cli.run_script()
    sys.stdout = old_stdout
    stdout_value = mystdout.getvalue()
    env_path = """'environment_path': """ + "'" + str(tmp_path) + "/env'"
    assert """'pem_filename': 'my_key.pem'""" in stdout_value
    assert env_path in stdout_value


# def test_example(tm):
#     old_stdout = sys.stdout
#     sys.stdout = mystdout = StringIO()
#     my_cli = CLI([
#         "my_key.pem",
#         "-v",
#         "-e",
#         os.path.join(tmp_path, 'env')])
#     my_cli.run_script()
#     sys.stdout = old_stdout
#     stdout_value = mystdout.getvalue()
