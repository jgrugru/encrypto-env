import argparse
from os import getcwd

from .EnvFile import EnvFile

cli_version = '1.0'


class CLI():
    """
    Class that filters through the command line options.
    The run_script function is the lead function, calling
    functions for each specified option.
    """

    def __init__(self, args):
        self.args = self.parse_args(args)
        self.environment_path = getcwd() + '/env/'

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
            help="Specify the name of the \
                  .env file stored in the filepath environmental_path/env"
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

    def create_env_file(self):
        if self.args.environment_path:
            self.environment_path = self.args.environment_path

        if self.args.pem_file and self.args.dot_env_file:
            self.env_file = EnvFile(self.environment_path,
                                    self.args.no_key,
                                    filename=self.args.dot_env_file,
                                    pem_filename=self.args.pem_file)
        else:
            if self.args.pem_file:
                self.env_file = EnvFile(self.environment_path,
                                        self.args.no_key,
                                        pem_filename=self.args.pem_file)
            elif self.args.dot_env_file:
                self.env_file = EnvFile(self.environment_path,
                                        self.args.no_key,
                                        filename=self.args.dot_env_file)
            else:
                self.env_file = EnvFile(self.environment_path,
                                        self.args.no_key)

        self.env_file.create_filepath()

    def clear_option(self):
        if(self.args.clear):
            self.env_file.clear_file()

    def add_variable_option(self):
        if self.args.add_variable:
            for x in self.args.add_variable:
                if not self.env_file.is_empty():
                    self.env_file.append_data_to_file('\n' + x)
                else:
                    self.env_file.append_data_to_file(x)

    def list_variable_option(self):
        if self.args.list_variables:
            self.env_file.parse_env_var_str(
                self.env_file.decrypt_data_from_env_file())

    def run_script(self):

        # Print the variables with verbose mode.
        if self.args.verbose:
            print(vars(self.args))

        # --pem_file
        # --dot-env-file
        # --environment-path
        # --no-key
        # creates pem_file if it doesn't exist
        self.create_env_file()

        # --clear
        self.clear_option()

        # use the --add-variable option
        self.add_variable_option()

        if self.args.Encrypt and not self.env_file.is_binary():
            self.env_file.encrypt()

        self.list_variable_option()

        if self.args.Decrypt and self.env_file.is_binary():
            self.env_file.decrypt()
