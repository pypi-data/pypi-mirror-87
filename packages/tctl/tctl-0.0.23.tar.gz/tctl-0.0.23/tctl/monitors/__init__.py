#!/usr/bin/env python

import click
from .. import utils
from . import crud


commands = {
    "ls": "    Retreive monitors list",
    "list": "  Retreive monitors list",
    "new": "   Create new monitor",
    "delete": "Delete monitor (via --monitor|-m <MONITOR-ID>)",
    "rm": "    Delete monitor (via --monitor|-m <MONITOR-ID>)",
}

rules = utils.args_actions()
rules.add_required("list", {"strategy": ["-s", "--strategy"]})
rules.add_optional("new", {"type": ["-t", "--type"]})

for command in ["list", "new"]:
    rules.add_required(command, {"strategy": ["-s", "--strategy"]})

for command in ["info", "update", "delete"]:
    rules.add_required(command, {"monitor": ["-m", "--monitor"]})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


@click.group()
def cli():
    pass


# router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=options_validator)
def monitors(options):
    """List, create, update, or delete monitors"""
    command, options = options
    # print(command, options)

    if command in ["ls", "list"]:
        crud.monitors_list(options)

    elif command == "new":
        crud.monitor_create(options)

    elif command in ["rm", "delete"]:
        crud.monitor_delete(options)
