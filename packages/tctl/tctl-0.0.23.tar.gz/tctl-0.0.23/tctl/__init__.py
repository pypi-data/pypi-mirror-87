import click
import sys

from pathlib import Path
__env_path__ = Path.home() / ".tradologics"

from .env import ENVIRONMENT
if ENVIRONMENT == "dev":
    __env_path__ = Path.home() / ".tradologics-dev"

# internals
from . import version
from . import config
from . import brokers
from . import accounts
from . import assets
from . import strategies
from . import tradehooks
from . import monitors
from . import orders
from . import trading
from . import tokens
from . import upgrade
from . import me


if "--version" in sys.argv or "-V" in sys.argv:
    click.echo("\ntctl {version}".format(version=version.version))
    click.echo("Copyrights (c) Tradologics, Inc.")
    click.echo("https://tradologics.com")
    sys.exit()


cli = click.CommandCollection(sources=[
    config.cli,
    brokers.cli,
    accounts.cli,
    assets.cli,
    strategies.cli,
    tradehooks.cli,
    monitors.cli,
    orders.cli,
    trading.cli,
    tokens.cli,
    upgrade.cli,
    me.cli,
])


__version__ = version.version
__author__ = "Tradologics, Inc"

__all__ = ['cli']
