import click

from .login import login
from .install import install
from .upload import upload
from .env import env
from ..compatibility import COILED_VERSION

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(COILED_VERSION, message="%(version)s")
def cli():
    """Coiled command line tool"""
    pass


cli.add_command(login)
cli.add_command(install)
cli.add_command(upload)
cli.add_command(env)
