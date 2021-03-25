import os
from sys import argv, path

path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
            os.path.pardir)))

from encryptoenv.CLI import CLI

if __name__ == "__main__":
    my_cli = CLI(argv[1:])
    my_cli.run_script()

# flake8: noqa