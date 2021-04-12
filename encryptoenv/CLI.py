import argparse
from os import path

from .EnvDir import EnvDir
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

    def get_pem_file(self):
        return self.pem_file

    def get_environment_path(self):
        return self.env_dir

    def clear_option(self):
        if(self.args.clear):
            self.env_file.clear_file()

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
            self.env_dir.create_filepath()
            if not self.args.no_key:
                self.pem_file.gen_pem_file()

    def create_env_file(self):
        # If the name is specified, a blank will be created.
        self.env_file = EnvFile(self.env_dir.get_filepath())#,
                                # pem_filename=self.args.pem_file,
                                # filename=self.args.dot_env_file)

        self.env_file.create_filepath()

    def blank_option(self):
        if self.args.blank:
            self.env_file.create_filepath()

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

        # Use the -e option to set the environment path.
        # This needs to be one of the first actions.
        # Pem_file and env_file require the env_path
        self.environmental_path_option()
        self.env_dir.create_filepath()
        
        # check --pem-file option
        # self.create_pem_file()

        # check --dot-env-file option and create env_file
        self.create_env_file()

        # use the --clear option
        self.clear_option()

        # check if the env dir exists. Else create env and pem file
        # self.create_dir_and_pem()

        # use the -b (blank) option
        self.blank_option()

        # if not self.args.no_key:
        #     self.env_file.set_encryptor()

        # use the --add-variable option
        self.add_variable_option()

        if self.args.Encrypt and not self.env_file.is_binary():
            self.env_file.encrypt()

        # self.list_variable_option()
        # breakpoint()
        if self.args.Decrypt and self.env_file.is_binary():
            print("*********************", "I'm inside")
            x = self.env_file.encryptor.decrypt_data(self.env_file.get_bytes_from_file())
            print("*******", x)
