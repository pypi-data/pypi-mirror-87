#!/usr/bin/env python

import click
from .. import utils
from . import crud
from . import crud_versions


commands = {
    "ls": "      Retreive list of strategies",
    "list": "    Retreive list of strategies",
    "info": "    Show strategy information (via --strategy|-s <STRATEGY-ID>)",
    "new": "     Create new strategy",
    "update": "  Update existing strategy (via --strategy|-s <STRATEGY-ID>)",
    "delete": "  Delete strategy (via --strategy|-s <STRATEGY-ID>)",
    "rm": "      Delete strategy (via --strategy|-s <STRATEGY-ID>)",
    "deploy": "  Deploy code to a strategy (via --strategy|-s <STRATEGY-ID>, optional: --lang <LANGUAGE>)",
    "set-mode": "Change the mode of the strategy (via --strategy|-s <STRATEGY-ID>)",
    "start": "   Starts a strategy (via --strategy|-s <STRATEGY-ID>)",
    "stop": "    Stops a strategy (via --strategy|-s <STRATEGY-ID>)",
    "status": "  Display strategy status (via --strategy|-s <STRATEGY-ID>, optional: --start <YYYY-MM-DD>, --end <YYYY-MM-DD>)",
    "log": "     Show strategy deployment logs (via --strategy|-s <STRATEGY-ID>, optional: --lines)",
    "stats": "   Show strategy statistics (via --strategy|-s <STRATEGY-ID>, optional: --download <PATH>)",
}

rules = utils.args_actions()
for command in ["info", "update", "delete", "status", "log",
                "set-mode", "start", "stop", "stats",  "deploy"]:
    rules.add_required(command, {"strategy": ["-s", "--strategy"]})

rules.add_optional("deploy", {"lang": ["-l", "--lang"]})
rules.add_optional("set-mode", {"mode": ["-m", "--mode"]})
rules.add_optional("log", {"lines": ["-l", "--lines"]})
rules.add_optional("stats", {
    "start": ["--start"],
    "end": ["--end"],
})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


@click.group()
def cli():
    pass


# router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=options_validator)
def strategies(options):
    """List, create, update, delete, deploy, start and stop strategies"""
    command, options = options
    # print(command, options)

    if command in ["ls", "list"]:
        crud.strategies_list(options)

    elif command == "info":
        crud.strategy_info(options)

    elif command == "status":
        crud.strategy_status(options)

    elif command == "log":
        crud.strategy_log(options)

    elif command == "update":
        crud.strategy_update(options)

    elif command in ["rm", "delete"]:
        crud.strategy_delete(options)

    elif command == "set-mode":
        crud.strategy_set_mode(options)

    elif command == "new":
        crud.strategy_create(options)

    elif command == "start":
        crud.strategy_start(options)

    elif command == "stop":
        crud.strategy_stop(options)

    elif command == "deploy":
        crud_versions.strategy_deploy(options)

    elif command == "stats":
        crud.strategy_stats(options)
