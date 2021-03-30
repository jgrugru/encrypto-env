from os import getcwd
from .FileObject import FileObject


class EnvDir(FileObject):
    """
    This class is an abstraction of the
    environmental path. Inherits from
    FileOBject. The default environment
    path is ./env. This can be overwritten
    with the -e or --environment-path.
    EX) encryptoenv "my_key.pem" -e "/tmp/env"
    """
    default_path = getcwd() + '/env/'

    def __init__(self, filepath=default_path):
        self.filepath = filepath