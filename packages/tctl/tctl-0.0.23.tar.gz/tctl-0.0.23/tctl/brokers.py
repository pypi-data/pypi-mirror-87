#!/usr/bin/env python

import click
from . import utils
from . import remote


@click.group()
def cli():
    pass


@cli.command()
@click.argument('list', required=False)
@click.argument('ls', required=False)
@click.option('--raw', is_flag=True, help="Present raw results?")
def brokers(list=None, ls=None, raw=False):
    """List supported brokers list"""
    data, errors = remote.api.get("/brokers")

    if raw:
        click.echo(utils.to_json(data, errors))
        return

    click.echo(utils.to_table(data))
