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

    def write_data_to_file(self, data, verbose_flag=False):
        # self.clear_file()
        if not self.is_binary():
            self.clear_file()
            with open(self.filepath, 'wb') as env_file:
                env_file.write(data)
                env_file.close()
            if verbose_flag:
                print("Wrote encrypted data to " + str(self))
        else:
            self.delete_file()
            self.create_filepath()
            with open(self.filepath, 'w') as env_file:
                env_file.write(data)
                env_file.close()
            if verbose_flag:
                print("Wrote decrypted data to " + str(self))