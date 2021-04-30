from os import path, environ, getcwd
from fileflamingo.EncryptionFile import BaseFile
from fileflamingo.EncryptionFile import EncryptionFile
from fileflamingo.RSAFile import RSAFile

line_separator = b'aJh@WDFWDg-#4jZr'


class EnvFile(EncryptionFile):
    """
    An abstraction of the '/env/.env' file.
    Inherits all the functions from EncryptionFile.
    """

    cwd = getcwd() + '/env/'

    def __init__(self,
                 environment_path=cwd,
                 filename='.env',
                 pem_filename='my_key.pem',
                 no_key=False):

        if not str(environment_path)[len(environment_path)-1] == '/':
            environment_path = environment_path + '/'

        self.environment_path = BaseFile(environment_path)
        self.environment_path.create_filepath()

        if not no_key:
            self.rsa_file = RSAFile(
                path.join(self.environment_path.get_filepath(), pem_filename))
            if not self.rsa_file.filepath_exists():
                self.rsa_file.create_filepath()
                self.rsa_file.gen_pem_file()

            super().__init__(
                path.join(self.environment_path.get_filepath(), filename),
                path.join(self.environment_path.get_filepath(), pem_filename))
        else:
            self.filepath = path.join(
                self.environment_path.get_filepath(), filename)
            self.is_encrypted = False

        self.create_filepath()

    def get_environment_path(self):
        return self.environment_path

    def split_str_by_equalsign(self, variable):
        return variable.split("=")

    def add_variables_as_bytes(self, variable_list):
        for var in variable_list:
            encrypted_line = self.encrypt_line(var)
            self.write_byte_line_to_file(encrypted_line)

    def add_variables_as_text(self, variable_list):
        if not self.is_empty():             # this counteracts the strip()
            self.append_text_to_file('\n')
        for var in variable_list:
            var = var.strip()
            text_line = self.write_text_line_to_file(var)

    def set_environment_variable(self, variable):
        environ[variable[0]] = variable[1]

    def create_environment_variables(self):
        for variable in self.get_decrypted_lines_as_list():
            self.set_environment_variable(
                self.split_str_by_equalsign(variable))
