from os import path, mkdir, getcwd
from FileObject import FileObject


class EnvDir(FileObject):

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
            print("Successfully created the directory %s " % path)
