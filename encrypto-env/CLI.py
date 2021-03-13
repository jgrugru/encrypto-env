import argparse
from EnvPath import EnvPath
from PemFileManager import PemFileManager


my_parser = argparse.ArgumentParser(
    prog='encrypto-env',
    usage='%(prog)s [options] path',
    description="Encrypt the contents of your .env file \
    with a key stored in a pem file.",
    epilog='Please let me know of any improvements \
        that could be made. |\
        email: jeff.gruenbaum@gmail.com | github: @jgrugru',
    fromfile_prefix_chars='@'
)

my_parser.version = '1.0'

my_parser.add_argument(
    "pem_filename",
    metavar="pem_filename",
    type=str,
    help="The pem filepath relative to the env folder"
)

my_parser.add_argument(
    '-e',
    '--environment-path',
    metavar="env_path",
    type=str,
    help="Default is 'env' dir. This is where the program looks for the pem."
)

my_parser.add_argument(
    '-E',
    '--Encrypt',
    action='store_true',
    help="Encrypt .env file that already exists."
)

my_parser.add_argument(
    '-D',
    '--Decrypt',
    action='store_true',
    help='Decrypt .env file and output variables.'
)

my_parser.add_argument(
    '-b',
    '--blank',
    action='store_true',
    help="Create blank .env file if one does not exist."
)

my_parser.add_argument(
    '-a',
    '--add-variable',
    action='store',
    metavar="var",
    type=int,
    nargs='+',
    help="Add variables that will be encrypted to the .env file."
)

my_parser.add_argument(
    '--clear',
    action='store_true',
    help="Clear the .env file of all variables."
)

my_parser.add_argument(
    '-v',
    '--version',
    action="version"
)

args = my_parser.parse_args()

print(vars(args))

pem_filepath = args.pem_filename

# if env_filepath:
#     env_path.set_env_path(env_filepath)

# # Checks if env folder exists or creates ones.
# env_path.create_env_path()
# pem_file = PemFileManager(env_path, pem_filename)

# if pem_file.pem_file_exists():
#     typer.echo("Pem already exists at " + pem_file.filepath)
# else:
#     pem_file.gen_pem_file()
#     typer.echo("Created pem file at " + pem_file.filepath)

# for x in kwargs:
#     print(x)