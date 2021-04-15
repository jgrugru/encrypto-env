from os import path, environ
from fileflamingo.EncryptionFile import BaseFile
from fileflamingo.EncryptionFile import EncryptionFile
from fileflamingo.RSAFile import RSAFile


class EnvFile(EncryptionFile):
    """
    An abstraction of the '/env/.env' file.
    Inherits all the functions from EncryptionFile.
    """

    def __init__(self,
                 environment_path,
                 filename='.env',
                 pem_filename='my_key.pem',
                 no_key=False):

    # need to set all argument for init to be kwargs, they need to be optional
    # so I can create envfile with only environment path.
    # no-key should default to false.

        self.environment_path = BaseFile(environment_path)
        self.environment_path.create_filepath()

        if not no_key:
            self.rsa_file = RSAFile(path.join(environment_path, pem_filename))
            if not self.rsa_file.filepath_exists():
                self.rsa_file.create_filepath()
                self.rsa_file.gen_pem_file()

            super().__init__(
                path.join(environment_path, filename),
                path.join(environment_path, pem_filename))
        else:
            self.filepath = path.join(environment_path, filename)
            self.is_encrypted = False

    def get_environment_path(self):
        return self.environment_path

    def append_variables_to_txt_str(self, text_str, variable_list):
        appending_str = text_str
        for var in variable_list:
            appending_str += var + '\n'

        return appending_str

    def split_str_by_equalsign(self, variable):
        return variable.split("=")

    def get_decrypted_data(self):
        decrypted_data = self.encryptor.decrypt_data(
            self.get_bytes_from_file())
        return decrypted_data

    def add_variables_as_bytes(self, variable_list):
        decrypted_data = self.get_decrypted_data()
        data_to_encrypt = self.append_variables_to_txt_str(
            decrypted_data,
            variable_list)
        encrypted_data = self.encryptor.encrypt_data(data_to_encrypt)
        self.write_bytes_to_file(encrypted_data)

    def set_environment_variable(self, variable):
        environ[variable[0]] = variable[1]

    def create_environment_variables(self):
        for variable in self.get_decrypted_data().split('\n'):
            self.set_environment_variable(self.split_str_by_equalsign(variable))
