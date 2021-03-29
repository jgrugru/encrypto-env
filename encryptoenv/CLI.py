import argparse

from .Encryptor import Encryptor
from .EnvDir import EnvDir
from .EnvFile import EnvFile
from .PemFile import PemFile

cli_version = '1.0'


class CLI():
    """
    Class that filters through the command line options.
    The run_script function is the lead function, calling
    functions for each specified option.
    """

    def __init__(self, args):
        self.args = self.parse_args(args)
        self.env_dir = EnvDir()
        self.pem_file = None

    def parse_args(self, args):
        self.my_parser = argparse.ArgumentParser(
            prog='encrypto-env',
            usage='%(prog)s [options] path',
            description="Encrypt the contents of your .env file \
            with an RSA key.",
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
            # "pem_filename",
            "-p",
            "--pem-file",
            metavar="pem_path",
            type=str,
            help="The pem filepath relative to the environment path folder")

        self.my_parser.add_argument(
            '--environment-path',
            metavar="env_path",
            type=str,
            help="Default is 'env' dir. This is where \
                  the program looks for the pem")

        self.my_parser.add_argument(
            '-b',
            '--blank',
            action='store_true',
            help="Create blank .env file")

        self.my_parser.add_argument(
            '-a',
            '--add-variable',
            action='store',
            metavar="var",
            type=str,
            nargs='+',
            help="Add variables to the .env file")

        self.my_parser.add_argument(
            '--clear',
            action='store_true',
            help="Clear the contents of the .env file")

        self.my_parser.add_argument(
            '--dot-env-file',
            metavar="dot_env_file",
            action="store",
            help="Specify the name of the .env file"
        )

        self.my_parser.add_argument(
            '-l',
            '--list-variables',
            action='store_true',
            help="List the variable names stored in the .env file"
        )

        self.my_parser.add_argument(
            '--no-key',
            action='store_true',
            help="Disables creation of my_key.pem file"
        )

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
            help="Encrypt .env file")

        self.my_group.add_argument(
            '-D',
            '--Decrypt',
            action='store_true',
            help='Decrypt .env file')

    def get_env_file(self):
        return self.env_file

    def get_pem_file(self):
        return self.pem_file

    def get_environment_path(self):
        return self.env_dir

    def parse_env_var_str(self, env_file_str):
        for env_var in env_file_str.split("\n"):
            if not env_var == "":
                print(env_var.split("=")[0])

    def clear_option(self):
        if(self.args.clear):
            self.env_file.clear_file(self.args.verbose)

    def environmental_path_option(self):
        if self.args.environment_path:
            self.env_dir.set_filepath(self.args.environment_path)
            if self.args.verbose:
                print("Set environemental path to "
                      + self.env_dir.get_filepath())

    def create_dir_and_pem(self):
        if self.env_dir.filepath_exists():
            if(self.args.verbose):
                print(self.env_dir.get_filepath() + " already exists.")
        else:
            self.env_dir.create_filepath(self.args.verbose)
            if not self.args.no_key:
                self.pem_file.gen_pem_file(self.args.verbose)

    def create_env_file_object(self):
        if not self.args.dot_env_file:
            self.env_file = EnvFile(self.env_dir.get_filepath())
        else:
            # If the name is specified, a blank should be created.
            self.args.blank = True
            self.env_file = EnvFile(self.env_dir.get_filepath(),
                                    self.args.dot_env_file)

    def create_pem_file_object(self):
        if self.args.pem_file:
            self.pem_file = PemFile(self.env_dir.get_filepath(),
                                    self.args.pem_file)
        else:
            self.pem_file = PemFile(self.env_dir.get_filepath())

    def blank_option(self):
        if self.args.blank:
            self.env_file.create_filepath(self.args.verbose)

    def add_variables_to_txt_file(self):
        self.env_file.append_data_to_file(
            self.env_file.append_variables_to_txt_str(
                self.env_file.get_contents_of_file(),
                self.args.add_variable,
                self.args.verbose))

    def add_variables_to_binary_file(self):
        decrypted_data = self.decrypt_data_from_env_file()
        data_to_encrypt = self.env_file.append_variables_to_txt_str(
            decrypted_data,
            self.args.add_variable,
            self.args.verbose)
        encrypted_data = self.encryptor.encrypt_data(data_to_encrypt)
        self.env_file.write_data_to_file(encrypted_data)

    def add_variable_option(self):
        if self.args.add_variable:
            if not self.env_file.filepath_exists():
                self.env_file.create_filepath()
            if not self.env_file.is_binary():
                self.add_variables_to_txt_file()
            else:
                self.add_variables_to_binary_file()

    def list_variable_option(self):
        if self.args.list_variables:
            self.parse_env_var_str(self.decrypt_data_from_env_file())

    def encrypt_data_from_env_file(self):
        x = self.encryptor.encrypt_data(self.env_file.get_contents_of_file())
        return x

    def encrypt_env_file(self):
        if self.env_file.filepath_exists():
            encrypted_data = self.encrypt_data_from_env_file()
            self.env_file.write_data_to_file(
                encrypted_data,
                verbose_flag=self.args.verbose)
        else:
            print(self.env_file.get_filepath + " does not exist.")

    def decrypt_data_from_env_file(self):
        decrypted_data = None

        if self.env_file.filepath_exists():
            decrypted_data = self.encryptor.decrypt_data(
                self.env_file.get_contents_of_file())
        else:
            print(self.env_file.get_filepath + " does not exist.")

        return decrypted_data

    def run_script(self):

        # Print the variables with verbose mode.
        if self.args.verbose:
            print(vars(self.args))

        # Use the -e option to set the environment path.
        # This needs to be one of the first actions.
        # Pem_file and env_file require the env_path
        self.environmental_path_option()

        # check --pem-file option
        self.create_pem_file_object()

        # check --dot-env-file option and create env_file
        self.create_env_file_object()

        # use the --clear option
        self.clear_option()

        # check if the env dir exists. Else create env and pem file
        self.create_dir_and_pem()

        # use the -b (blank) option
        self.blank_option()

        if not self.args.no_key:
            self.encryptor = Encryptor(self.pem_file.get_key())

        # use the --add-variable option
        self.add_variable_option()

        if self.pem_file.filepath_exists():
            if self.args.Encrypt and not self.env_file.is_binary():
                self.encrypt_env_file()

            self.list_variable_option()

            if self.args.Decrypt and self.env_file.is_binary():
                self.decrypt_data()
