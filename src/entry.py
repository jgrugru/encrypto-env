import rich_click as click
from rich_click import rich_click
rich_click.USE_RICH_MARKUP = True

# import click
from typing import Union
VERSION = "0.1.0"

@click.command()
@click.version_option(VERSION, "--version", "-v")
@click.help_option("-h", "--help")
@click.option("--show", "-s", is_flag=True, help="List all the variables in the .env file.")
@click.option("--add", "-a", help="Add a variable to .env file. Format: [italic]MYVAR=hello[/]", multiple=True)
def cli(show: bool, add):
    if len(add) != 0:
        click.echo(f"Adding variables {add=}")
    if show:
        print("Printing all the env vars")

# @cli.command(name="add", help="Add a variable to .env file: [italic]encryptoenv add MYVAR=hello[/]")
# @click.argument("variable", nargs=-1, type=str)
# def add_variable(variable: Union[str, list[str]]):
#     click.echo(f'adding a variable to .env file {variable}')

# @cli.command(name="list", help="List all the variables in the .env: [italic]encryptoenv list[/]")
# def add_variable():
#     click.echo('adding a variable to .env file')


if __name__ == '__main__':
    cli()


# @click.command()
# @click.version_option(version=VERSION)
# @click.option("--add-variable", "-a", default=None)
# def main(add_variable: str):
#     env_filepath = find_dotenv(raise_error_if_not_found=True)
#     print(env_filepath)
