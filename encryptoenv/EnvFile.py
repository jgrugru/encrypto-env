from os import path
from .FileObject import FileObject


class EnvFile(FileObject):

    def __init__(self, environment_path, filename='.env'):
        self.filepath = path.join(environment_path, filename)

    def create_filepath(self, verbose_flag):
        if path.exists(self.filepath) and verbose_flag:
            print("A file already exists at " + self.filepath)
        else:
            open(self.filepath, 'a').close()

    def write_variables_to_file(self, variable_list, verbose_flag):
        with open(self.filepath, 'a') as env_file:
            for var in variable_list:
                if verbose_flag:
                    print("Writing " + var + " to " + self.filepath)
                env_file.write(var + '\n')

    def clear_file(self, verbose_flag):
        if self.filepath_exists():
            open(self.filepath, 'w').close()
            if verbose_flag:
                print("Clearing the contents of " + self.filepath)
        else:
            print("The file could not be cleared because "
                  + self.filepath + " does not exist.")
