from os import path
from pathlib import Path
import struct
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

    def clear_file(self, verbose_flag=False):
        if self.filepath_exists():
            open(self.filepath, 'w').close()
            if verbose_flag:
                print("Clearing the contents of " + self.filepath)
        else:
            print("The file could not be cleared because "
                  + self.filepath + " does not exist.")

    def write_data_to_file(self, data):
        # self.clear_file()
        with open(self.filepath, 'w') as env_file:
            env_file.write(data)
            env_file.close()

    def get_binary_contents(self, verbose_flag=False):
        data = Path(self.filepath).read_bytes()
        ints = struct.unpack('iiii', data[:16])
        return ints