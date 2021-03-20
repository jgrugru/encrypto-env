import argparse
import os
from sys import path
from Crypto.Cipher import Salsa20
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode,b64encode

path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
            os.path.pardir)))

from encryptoenv.EnvDir import EnvDir
from encryptoenv.EnvFile import EnvFile
from encryptoenv.PemFile import PemFile
from encryptoenv.Encryptor import Encryptor

cli_version = '1.0'


class CLI():

    def __init__(self, args):
        self.args = self.parse_args(args)
        self.env_dir = EnvDir()

    def parse_args(self, args):
        self.my_parser = argparse.ArgumentParser(
            prog='encrypto-env',
            usage='%(prog)s [options] path',
            description="Encrypt the contents of your .env file \
            with a key stored in a pem file.",
            epilog='Please let me know of any improvements \
                that could be made. |\
                email: jeff.gruenbaum@gmail.com | github: @jgrugru',
            fromfile_prefix_chars='@')

        self.my_group = self.my_parser.add_mutually_exclusive_group(
            required=False)

        self.my_parser.version = cli_version

        self.add_arguments()

        return self.my_parser.parse_args(args)

    def add_arguments(self):
        self.my_parser.add_argument(
            "pem_filename",
            metavar="pem_filename",
            type=str,
            help="The pem filepath relative to the env folder")

        self.my_parser.add_argument(
            '-e',
            '--environment-path',
            metavar="env_path",
            type=str,
            help="Default is 'env' dir. This is where \
                  the program looks for the pem.")

        self.my_parser.add_argument(
            '-b',
            '--blank',
            action='store_true',
            help="Create blank .env file if one does not exist.")

        self.my_parser.add_argument(
            '-a',
            '--add-variable',
            action='store',
            metavar="var",
            type=str,
            nargs='+',
            help="Add variables that will be encrypted to the .env file.")

        self.my_parser.add_argument(
            '--clear',
            action='store_true',
            help="Clear the .env file of all variables.")

        self.my_parser.add_argument(
            '-n',
            '--name',
            metavar="name",
            action="store",
            help="Specify the name of the '.env' file."
        )

        # my_parser.add_argument(
        #     '--directory-name',
        #     action="store",
        #     help="Specify the name of the dir for .env to be stored. \
        #           It will be placed in the environment path specified."
        # )

        self.my_parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help="Verbose ouptut")

        self.my_parser.add_argument(
            '--version',
            action="version")

        self.my_group.add_argument(
            '-E',
            '--Encrypt',
            action='store_true',
            help="Encrypt .env file that already exists.")

        self.my_group.add_argument(
            '-D',
            '--Decrypt',
            action='store_true',
            help='Decrypt .env file and output variables.')

    def clear_option(self, env_file):
        if(self.args.clear):
            env_file.clear_file(self.args.verbose)

    def set_environmental_path(self):
        if self.args.environment_path:
            self.env_dir.set_filepath(self.args.environment_path)
            if self.args.verbose:
                print("Set environemental path to "
                      + self.env_dir.get_filepath())

    def create_dir_and_pem(self, pem_file):
        if self.env_dir.filepath_exists():
            if(self.args.verbose):
                print(self.env_dir.get_filepath() + " already exists.")
        else:
            self.env_dir.create_filepath(self.args.verbose)
            pem_file.gen_pem_file(self.args.verbose)

    def create_env_file_object(self):
        if not self.args.name:
            return EnvFile(self.env_dir.get_filepath())
        else:
            return EnvFile(self.env_dir.get_filepath(), self.args.name)

    def encrypt_env_file(self, encryptor, env_file):
        if env_file.filepath_exists():
            encrypted_data = encryptor.encrypt_data(env_file.get_contents_of_file())
            env_file.write_data_to_file(encrypted_data)
        else:
            print(env_file.get_filepath + " does not exist.")

    # def decrypt_env_file(self, encryptor, env_file):
    #     if env_file.filepath_exists():
    #         decrypted_data = encryptor.decrypt_data(env_file.get_contents_of_file()
    #         env_file.write_data_to_file(decrypted_data)
    #     else:
    #         print(env_file.get_filepath + " does not exist.")

    def run_script(self):

        # Use the -e option to set the environment path.
        # This needs to be one of the first actions.
        # Pem_file and env_file require the env_path
        self.set_environmental_path()

        # Print the variables with verbose mode.
        if self.args.verbose:
            print(vars(self.args))

        pem_file = PemFile(self.env_dir.get_filepath(), self.args.pem_filename)

        env_file = self.create_env_file_object()

        encryptor = Encryptor(pem_file.get_key())

        # use the --clear option
        self.clear_option(env_file)

        # check if the env dir exists. Else create env and pem file
        self.create_dir_and_pem(pem_file)

        # use the -b (blank) option
        if self.args.blank:
            env_file.create_filepath(self.args.verbose)

        # use the --add-variable option
        if self.args.add_variable:
            env_file.write_variables_to_file(self.args.add_variable,
                                             self.args.verbose)

        if self.args.Encrypt:
            self.encrypt_env_file(encryptor, env_file)

        if self.args.Decrypt:
            self.decrypt_env_file(encryptor, env_file)

        # if self.args.verbose:
        #     print("TESTING",'\n-------------')
        #     self.encrypt_env_file(encryptor, env_file)
