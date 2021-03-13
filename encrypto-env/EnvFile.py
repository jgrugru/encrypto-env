from os import path, getcwd, remove
from FileObject import FileObject

class EnvFile(FileObject):

    default_path = path.join(getcwd(), 'env', '.env')


    def __init__(self, filepath=default_path):
        self.filepath = filepath