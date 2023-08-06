import typer
from pathlib import Path
import os
from pear.configuration import Configuration

app = typer.Typer()


@app.command()
def format():
    typer.echo("Formatting files.")
    config = Configuration(cwd())
    for file in config.files():
        file.write()


def cwd() -> Path:
    return Path(os.getcwd()).joinpath('pear.json')


def main():
    app()


if __name__ == "__main__":
    main()
