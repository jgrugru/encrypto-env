from os import path
from .FileObject import FileObject


class EnvFile(FileObject):
    """
    An abstraction of the '/env/.env' file.
    Inherits all the functions from FileObject. Extends
    the class with functions:
    -WRITE_VARIABLES_TO_FILE: writes the variables that
    are passed from the '-a' option.
    EX) encryptoenv "my_key.pem" -a "test=1234" "test1=12345"
     --> will write these variables to the '/env/.env' file.
    -WRITE_DATA_TO_FILE: Checks if the file is binary (is encrypted).
    If encrypted, clear the file and then write back the
    data as text.
    If decrypted, clear the file and then write the data as
    bytes to the file.
    """

    def __init__(self, environment_path, filename='.env'):
        self.filepath = path.join(environment_path, filename)  

    def write_data_to_file(self, data, verbose_flag=False):
        self.clear_file()

        if not self.is_binary():
            with open(self.filepath, 'wb') as env_file:
                env_file.write(data)
                env_file.close()
            if verbose_flag:
                print("Wrote encrypted data to " + str(self))
        else:
            with open(self.filepath, 'w') as env_file:
                env_file.write(data)
                env_file.close()
            if verbose_flag:
                print("Wrote decrypted data to " + str(self))
