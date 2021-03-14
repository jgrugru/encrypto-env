import argparse
import os
from sys import argv, path

path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             os.path.pardir)))
                                
from encryptoenv.EnvDir import EnvDir
from encryptoenv.EnvFile import EnvFile
from encryptoenv.PemFile import PemFile

cli_version = '1.0'

def parse_args(args):

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

    my_parser = add_arguments(my_parser)
    
    return my_parser.parse_args(args)


def add_arguments(my_parser):
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
        help="Default is 'env' dir. This is where the program looks for the pem.")

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
        type=int,
        nargs='+',
        help="Add variables that will be encrypted to the .env file.")

    my_parser.add_argument(
        '--clear',
        action='store_true',
        help="Clear the .env file of all variables.")

    my_parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help="Verbose ouptut")

    my_parser.add_argument(
        '--version',
        action="version")

    return my_parser


env_path = EnvDir()

args = parse_args(argv[1:])

if args.verbose:
    print(vars(args))

pem_filepath = args.pem_filename

# use the --clear option
if(args.clear):
    if(args.verbose):
        print("Clearing the .env file.")

# use the -e option
if args.environment_path:
    env_path.set_filepath(args.environment_path)

pem_file = PemFile(env_path, pem_filepath)

# check if the env dir exists. Else create env and pem file
if env_path.filepath_exists():
    if(args.verbose):
        print(env_path.get_filepath() + " already exists.")
else:
    env_path.create_filepath(args.verbose)
    pem_file.gen_pem_file(args.verbose)