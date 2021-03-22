from os import path, mkdir, getcwd
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
    default_path = getcwd() + '/env'

    def __init__(self, filepath=default_path):
        self.filepath = filepath

    def create_filepath(self, verbose_flag):
        try:
            mkdir(self.filepath)
            if(verbose_flag):
                print("Created " + self.filepath)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            if verbose_flag:
                print("Successfully created the directory %s " % path)
