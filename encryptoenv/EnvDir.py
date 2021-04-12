from os import getcwd
from fileflamingo.BaseFile import BaseFile


class EnvDir(BaseFile):
    """
    This class is an abstraction of the
    environmental path. Inherits from
    BaseFile. The default environment
    path is ./env. This can be overwritten
    with the -e or --environment-path.
    Example:
    $ encryptoenv "my_key.pem" -e "/tmp/env"
    """
    default_path = getcwd() + '/env/'

    def __init__(self, filepath=default_path):
        self.filepath = filepath
