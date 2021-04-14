from os import path
from fileflamingo.EncryptionFile import BaseFile
from fileflamingo.EncryptionFile import EncryptionFile
from fileflamingo.RSAFile import RSAFile


class EnvFile(EncryptionFile):
    """
    An abstraction of the '/env/.env' file.
    Inherits all the functions from EncryptionFile.
    """

    def __init__(self,
                 filename,
                 pem_filename,
                 environment_path,
                 no_key):

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
