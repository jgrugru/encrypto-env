from os import path
from .FileObject import FileObject


class EnvFile(FileObject):

    def __init__(self, environment_path, filename='.env'):
        self.filepath = path.join(environment_path, filename)

    def write_variables_to_file(self, variable_list, verbose_flag=False):
        with open(self.filepath, 'a') as env_file:
            for var in variable_list:
                env_file.write(var + '\n')
                if verbose_flag:
                    print("Writing " + var + " to " + self.filepath)

    def clear_file(self, verbose_flag=False):
        if self.filepath_exists():
            open(self.filepath, 'w').close()
            if verbose_flag:
                print("Clearing the contents of " + self.filepath)
        else:
            print("The file could not be cleared because "
                  + self.filepath + " does not exist.")

    def write_data_to_file(self, data, is_encrypted=False):
        # self.clear_file()
        if is_encrypted:
            self.clear_file()
            with open(self.filepath, 'wb') as env_file:
                env_file.write(data)
                env_file.close()
        else:
            with open(self.filepath, 'w') as env_file:
                env_file.write(data)
                env_file.close()