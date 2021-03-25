import argparse

from .EnvDir import EnvDir
from .EnvFile import EnvFile
from .PemFile import PemFile
from .Encryptor import Encryptor

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
                  the program looks for the pem.")

        self.my_parser.add_argument(
            '-b',
            '--blank',
            action='store_true',
            help="Create blank .env file.")

        self.my_parser.add_argument(
            '-a',
            '--add-variable',
            action='store',
            metavar="var",
            type=str,
            nargs='+',
            help="Add variables to the .env file.")

        self.my_parser.add_argument(
            '--clear',
            action='store_true',
            help="Clear the contents of the .env file")

        self.my_parser.add_argument(
            '--dot-env-file',
            metavar="dot_env_file",
            action="store",
            help="Specify the name of the '.env' file."
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
            help="Encrypt .env file.")

        self.my_group.add_argument(
            '-D',
            '--Decrypt',
            action='store_true',
            help='Decrypt .env file.')

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
        if not self.args.dot_env_file:
            return EnvFile(self.env_dir.get_filepath())
        else:
            self.args.blank = True
            return EnvFile(self.env_dir.get_filepath(), self.args.dot_env_file)

    def encrypt_env_file(self, encryptor, env_file):
        if not env_file.is_binary():
            if env_file.filepath_exists():
                encrypted_data = encryptor.encrypt_data(
                    env_file.get_contents_of_file())
                env_file.write_data_to_file(
                    encrypted_data, verbose_flag=self.args.verbose)
            else:
                print(env_file.get_filepath + " does not exist.")
        else:
            if self.args.verbose:
                print(str(env_file) + " is already encrypted.")

    def decrypt_env_file(self, encryptor, env_file):
        if env_file.filepath_exists():
            decrypted_data = encryptor.decrypt_data(
                env_file.get_contents_of_file())
            print(decrypted_data)
            env_file.write_data_to_file(
                decrypted_data, verbose_flag=self.args.verbose)
        else:
            print(env_file.get_filepath + " does not exist.")

    def run_script(self):

        # Use the -e option to set the environment path.
        # This needs to be one of the first actions.
        # Pem_file and env_file require the env_path
        self.set_environmental_path()

        # Print the variables with verbose mode.
        if self.args.verbose:
            print(vars(self.args))

        if self.args.pem_file:
            pem_file = PemFile(self.env_dir.get_filepath(), self.args.pem_file)
        else:
            pem_file = PemFile(self.env_dir.get_filepath())

        env_file = self.create_env_file_object()

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

        encryptor = Encryptor(pem_file.get_key())

        if self.args.Encrypt:
            self.encrypt_env_file(encryptor, env_file)

        if self.args.Decrypt:
            self.decrypt_env_file(encryptor, env_file)
