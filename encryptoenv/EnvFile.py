from os import path, getcwd
from fileflamingo.EncryptionFile import BaseFile
from fileflamingo.EncryptionFile import EncryptionFile
from fileflamingo.RSAFile import RSAFile


class EnvFile(EncryptionFile):
    """
    An abstraction of the '/env/.env' file.
    Inherits all the functions from EncryptionFile. Extends
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

    default_environment_path = getcwd() + '/env/'

    def __init__(self, no_key,
                 environment_path=default_environment_path,
                 filename='.env',
                 pem_filename='my_key.pem'):

        self.environment_path = BaseFile(environment_path)
        self.environment_path.create_filepath()

        self.rsa_file = RSAFile(path.join(environment_path, pem_filename))
        if not self.rsa_file.filepath_exists():
            self.rsa_file.gen_pem_file()

        super().__init__(
            path.join(environment_path, filename),
            path.join(environment_path, pem_filename))

    def append_variables_to_txt_str(self, text_str, variable_list):
        appending_str = text_str
        for var in variable_list:
            appending_str += var + '\n'

        return appending_str

    def add_variables_as_txt(self, variable_list):
        self.append_data_to_file(
            self.append_variables_to_txt_str(
                self.get_contents_of_file(), variable_list))

    # def parse_env_var_str(self, env_file_str):
    #     for env_var in env_file_str.split("\n"):
    #         if not env_var == "":
    #             print(env_var.split("=")[0])

    # def decrypt_data_from_env_file(self):
    #     decrypted_data = None
    #     if self.filepath_exists():
    #         decrypted_data = self.encryptor.decrypt_data(
    #             self.get_contents_of_file())
    #     else:
    #         print(self.get_filepath() + " does not exist.")
    #     return decrypted_data

    # def encrypt_env_file(self):
    #     if self.filepath_exists():
    #         encrypted_data = self.encryptor.encrypt_data(
    #             self.get_contents_of_file())
    #         self.write_data_to_file(
    #             encrypted_data)
    #     else:
    #         print(self.get_filepath() + " does not exist.")

    # def add_variables_as_bytes(self, variable_list):
    #     decrypted_data = self.decrypt_data_from_env_file()
    #     data_to_encrypt = self.append_variables_to_txt_str(
    #         decrypted_data,
    #         variable_list)
    #     encrypted_data = self.encryptor.encrypt_data(data_to_encrypt)
    #     self.write_data_to_file(encrypted_data)
