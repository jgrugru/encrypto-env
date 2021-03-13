import typer
from typing import Optional

from EnvPath import EnvPath
from PemFileManager import PemFileManager


app = typer.Typer()
env_path = EnvPath()


@app.command()
def check_pem(pem_filename: str, env_filepath: Optional[str] = typer.Argument(None), **kwargs):
    """
    Accepts a single argument,
    -pem_filename (str: filepath that holds
    or will be created to hold the key)
    -env_filepath (Optional[str]: path to the directory holding env variables)
    """

    if env_filepath:
        env_path.set_env_path(env_filepath)

    # Checks if env folder exists or creates ones.
    env_path.create_env_path()
    pem_file = PemFileManager(env_path, pem_filename)

    if pem_file.pem_file_exists():
        typer.echo("Pem already exists at " + pem_file.filepath)
    else:
        pem_file.gen_pem_file()
        typer.echo("Created pem file at " + pem_file.filepath)

    for x in kwargs:
        print(x)


# @app.command()
# def add_env_var(pem_filepath: Optional[str] = typer.Argument(None), **kwargs):
#     """
#     If ran in the dir containing the 'env' folder,
#     the pem will be used automatically. Otherwise, the pem
#     filepath must be specified as the first parameter.
#     """

if __name__ == "__main__":
    app()
