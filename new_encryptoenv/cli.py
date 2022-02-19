import click
import os
import sys
import typing
from dotenv import find_dotenv


VERSION = "1.0.0"

@click.command()
@click.version_option(version=VERSION)
# @click.option("--add-variable", "-a")
def main():
    """Interact with your encrypted .env file."""
    env_filepath = find_dotenv(raise_error_if_not_found=True)
    print(env_filepath)

if __name__ == "__main__":
    main()
