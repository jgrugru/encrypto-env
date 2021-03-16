from os import path
from .FileObject import FileObject


class EnvFile(FileObject):

    def __init__(self, environment_path, filename='.env'):
        self.filepath = path.join(environment_path, filename)

    def create_filepath(self):
        open(self.filepath, 'a').close()
