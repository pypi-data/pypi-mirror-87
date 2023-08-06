#!/usr/bin/env python

import click
from .. import utils
from .. import remote
import urllib
from datetime import datetime
import pandas as pd
pd.options.display.float_format = '{:,}'.format


commands = {
    "ls": "      Retreive supported assets list (optional: --delisted)",
    "list": "    Retreive supported assets list (optional: --delisted)",
    "info": "    Show asset information (via --asset|-a <ASSET>, optional: --history)",
}

rules = utils.args_actions()
rules.add_flags("list", {"delisted": ["-d", "--delisted"]})
rules.add_flags("info", {"history": ["-h", "--history"]})
rules.add_required("info", {"asset": ["-a", "--asset"]})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


def assets_list(options):
    delisted = options.get("delisted", "False")
    if delisted:
        data, errors = remote.api.get("/assets?delisted=true")
    else:
        data, errors = remote.api.get("/assets")

    if options.get("raw"):
        click.echo_via_pager(utils.to_json(data))
        return

    df = pd.DataFrame(data)[[
        "ticker", "name", "exchange", "security_type",
        "delisted", "tuid", "tsid", "figi", "region", "currency"
    ]]

    if not delisted:
        df.drop(columns=["delisted"], inplace=True)

    df.rename(columns={
        "currency": "curr",
        "security_type": "type"
    }, inplace=True)

    df.sort_values("ticker", inplace=True)
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo_via_pager(utils.to_table(df))


def asset_info(options):
    history = options.get("history", False)
    endpoint = "/asset/{identifier}".format(
        identifier=options.first("asset").upper())

    if history:
        data, errors = remote.api.get(f"{endpoint}?history=true")
    else:
        data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    df = pd.DataFrame(data)[:1]
    df.drop(columns=["identifiers"], inplace=True)

    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def asset_bar(options):
    identifier = options.first("asset").upper()
    start, _ = utils.parse_date(options.first("start"))
    end, _ = utils.parse_date(
        options.get("end", [datetime.now().strftime("%Y-%m-%d")])[0])

    start = urllib.parse.quote(start)
    end = urllib.parse.quote(end)
    data, errors = remote.api.get(f"/pricing/bar/{identifier}/{start}/{end}")

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    df = pd.DataFrame([data])

    df.columns = [col.replace("_", " ").title() for col in df.columns]
    df = df[["Asset", "Start", "End", "O", "H", "L", "C", "V", "T", "W"]]
    df.columns = ["Asset", "Start", "End", "Open", "High",
                  "Low", "Close", "Volume", "Trades", "VWAP"]
    df.Asset = identifier
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))
