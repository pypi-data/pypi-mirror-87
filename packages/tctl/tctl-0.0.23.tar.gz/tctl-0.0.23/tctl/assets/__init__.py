#!/usr/bin/env python

import click
from . import assets_crud
from . import exchanges_crud
from . import bars_crud


@click.group()
def cli():
    pass


# asset router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=assets_crud.options_validator)
def assets(options):
    """List assets with misc. filtering options"""
    command, options = options

    if command in ["ls", "list"]:
        assets_crud.assets_list(options)

    elif command == "info":
        assets_crud.asset_info(options)


# asset router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=bars_crud.options_validator)
def bars(options):
    """List pricing information for assets"""
    command, options = options

    if command == "single":
        bars_crud.single(options)

    elif command == "history":
        bars_crud.history(options)


# asset router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=exchanges_crud.options_validator)
def exchanges(options):
    """Access exchange and calendar information"""
    command, options = options

    if command in ["ls", "list"]:
        exchanges_crud.exchanges_list(options)

    if command in ["info"]:
        exchanges_crud.exchange_info(options)

    if command in ["calendar"]:
        exchanges_crud.exchange_calendar(options)
