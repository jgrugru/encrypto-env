from os import path
from .FileObject import FileObject
from .Encryptor import Encryptor


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

    def __init__(self, environment_path, pem_file, filename='.env'):
        self.filepath = path.join(environment_path, filename)
        self.pem_file = pem_file
        self.encryptor = None

    def set_encryptor(self):
        self.encryptor = Encryptor(self.pem_file.get_key())

    def parse_env_var_str(self, env_file_str):
        for env_var in env_file_str.split("\n"):
            if not env_var == "":
                print(env_var.split("=")[0])

    def append_variables_to_txt_str(self, text_str, variable_list):
        appending_str = text_str
        for var in variable_list:
            appending_str += var + '\n'

        return appending_str

    def decrypt_data_from_env_file(self):
        decrypted_data = None
        if self.filepath_exists():
            decrypted_data = self.encryptor.decrypt_data(
                self.get_contents_of_file())
        else:
            print(self.get_filepath() + " does not exist.")
        return decrypted_data

    def encrypt_env_file(self):
        if self.filepath_exists():
            encrypted_data = self.encryptor.encrypt_data(
                self.get_contents_of_file())
            self.write_data_to_file(
                encrypted_data)
        else:
            print(self.get_filepath() + " does not exist.")

    def add_variables_as_txt(self, variable_list):
        self.append_data_to_file(
            self.append_variables_to_txt_str(
                self.get_contents_of_file(),
                variable_list))

    def add_variables_as_bytes(self, variable_list):
        decrypted_data = self.decrypt_data_from_env_file()
        data_to_encrypt = self.append_variables_to_txt_str(
            decrypted_data,
            variable_list)
        encrypted_data = self.encryptor.encrypt_data(data_to_encrypt)
        self.write_data_to_file(encrypted_data)
