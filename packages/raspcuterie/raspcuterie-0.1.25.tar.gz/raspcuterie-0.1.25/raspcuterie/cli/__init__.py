import os
from pathlib import Path

import click
from flask.cli import with_appcontext  # noqa

from .. import base_path
from ..devices import InputDevice, OutputDevice

os.environ.setdefault("FLASK_APP", "raspcuterie.app")

module_path = Path(__file__).parent


@click.group()
def cli():
    pass


from . import cron, fake, install  # noqa


@cli.command(short_help="Echo the current value of the input and output devices")
@with_appcontext
def devices():
    click.echo("Listing input devices:")
    click.echo("============================")

    for key, device in InputDevice.registry.items():
        try:
            click.echo(f"{key}: {device.read()}")
        except Exception as e:
            click.echo(click.style(f"{key}: {e}", fg="red"), err=True)

    click.echo("")
    click.echo("Listing output devices:")
    click.echo("============================")

    for key, device in OutputDevice.registry.items():
        try:
            click.echo(f"{key}: {device.value()}")
        except Exception as e:
            click.echo(click.style(f"{key}: {e}", fg="red"), err=True)


@cli.command(short_help="Edit the configuration file")
def config():

    file = base_path / "config.yaml"

    if not base_path.exists():
        base_path.mkdir(parents=True)

    if not file.exists():
        x = module_path / "config.yaml"
        with file.open("w") as f:
            f.write(x.read_text())

    click.echo(f"Editing {file} ")
    click.edit(filename=file)
