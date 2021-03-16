import argparse
import os
from sys import path

path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
            os.path.pardir)))

from encryptoenv.EnvDir import EnvDir
from encryptoenv.EnvFile import EnvFile
from encryptoenv.PemFile import PemFile

cli_version = '1.0'


class CLI():

    def __init__(self, args):
        self.args = self.parse_args(args)
        self.env_dir = EnvDir()

    def parse_args(self, args):
        my_parser = argparse.ArgumentParser(
            prog='encrypto-env',
            usage='%(prog)s [options] path',
            description="Encrypt the contents of your .env file \
            with a key stored in a pem file.",
            epilog='Please let me know of any improvements \
                that could be made. |\
                email: jeff.gruenbaum@gmail.com | github: @jgrugru',
            fromfile_prefix_chars='@')

        my_parser.version = cli_version

        my_parser = self.add_arguments(my_parser)

        return my_parser.parse_args(args)

    def add_arguments(self, my_parser):
        my_parser.add_argument(
            "pem_filename",
            metavar="pem_filename",
            type=str,
            help="The pem filepath relative to the env folder")

        my_parser.add_argument(
            '-e',
            '--environment-path',
            metavar="env_path",
            type=str,
            help="Default is 'env' dir. This is where \
                  the program looks for the pem.")

        my_parser.add_argument(
            '-E',
            '--Encrypt',
            action='store_true',
            help="Encrypt .env file that already exists.")

        my_parser.add_argument(
            '-D',
            '--Decrypt',
            action='store_true',
            help='Decrypt .env file and output variables.')

        my_parser.add_argument(
            '-b',
            '--blank',
            action='store_true',
            help="Create blank .env file if one does not exist.")

        my_parser.add_argument(
            '-a',
            '--add-variable',
            action='store',
            metavar="var",
            type=str,
            nargs='+',
            help="Add variables that will be encrypted to the .env file.")

        my_parser.add_argument(
            '--clear',
            action='store_true',
            help="Clear the .env file of all variables.")

        my_parser.add_argument(
            '-n',
            '--name',
            action="store",
            help="Specify the name of the '.env' file."
        )

        # my_parser.add_argument(
        #     '--directory-name',
        #     action="store",
        #     help="Specify the name of the dir for .env to be stored. \
        #           It will be placed in the environment path specified."
        # )

        my_parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help="Verbose ouptut")

        my_parser.add_argument(
            '--version',
            action="version")

        return my_parser

    def clear_option(self):
        if(self.args.clear):
            if(self.args.verbose):
                print("Clearing the .env file.")

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

        # use the --clear option
        self.clear_option()

        # check if the env dir exists. Else create env and pem file
        self.create_dir_and_pem(pem_file)

        if self.args.blank:
            env_file.create_filepath()
            print("Created file at " + env_file.get_filepath())
