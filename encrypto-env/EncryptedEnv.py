import typer

from EnvPath import EnvPath
from PemFileManager import PemFileManager


app = typer.Typer()
env_path = EnvPath()


@app.command()
def check_pem(filename: str):
    """
    Takes a single argument, filename.
    If the "my_file.pem" does not exist,
    one will be created.
    """

    # Checks if env folder exists or creates ones.
    env_path.create_env_path()
    pem_file = PemFileManager(env_path, filename)

    if pem_file.pem_file_exists():
        typer.echo("Pem already exists at " + pem_file.filepath)
    else:
        pem_file.gen_pem_file()
        typer.echo("Created pem file at " + pem_file.filepath)


if __name__ == "__main__":
    app()
