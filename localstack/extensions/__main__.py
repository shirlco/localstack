"""Simple internal CLI script used to initialize the extension venv from inside the container."""
import os

import click

from localstack import config

from . import repository


@click.group("extensions")
def cli():
    from localstack.utils.bootstrap import setup_logging

    setup_logging()


@cli.command("debug")
def debug():
    """
    Print debug information about localstack directories and run ``pip list`` in the extensions venv.
    """
    click.echo("Directories")
    click.echo("===========")
    for k, v in config.dirs.__dict__.items():
        click.echo(f"{k:13} {v}")

    click.echo()
    click.echo("Extensions venv")
    click.echo("===============")
    venv = repository.LOCALSTACK_VENV
    click.echo(f"localstack venv: {venv.venv_dir}")
    click.echo(f"  site-packages: {venv.site_dir if venv.exists else 'not initialized'}")
    venv = repository.get_extensions_venv()
    click.echo(f"extensions venv: {venv.venv_dir}")
    click.echo(f"  site-packages: {venv.site_dir if venv.exists else 'not initialized'}")

    click.echo()
    click.echo("pip list")
    click.echo("========")
    os.system(f"bash -c '. {venv.venv_dir}/bin/activate && pip list'")


@cli.command("init")
def init():
    """
    Initialize the extensions repository.
    """
    from . import repository

    repository.init()


if __name__ == "__main__":
    cli()
