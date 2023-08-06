#!/usr/bin/env python

import click
from .. import utils
from .. import remote
import urllib
from datetime import datetime
import pandas as pd
pd.options.display.float_format = '{:,}'.format


commands = {
    "single": "  Create single bar (via --asset|-a <ASSET> --start <YYYY-MM-DD>, optional: --end <YYYY-MM-DD>)",
    "history": " Update historical bar data for certain assets tradehook (via --asset|-a <ASSET>)",
}

rules = utils.args_actions()
rules.add_required("single", {
    "asset": ["-a", "--asset"],
    "start": ["--start"],
})
rules.add_optional("single", {"end": ["--end"]})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


def history(options):
    click.echo(click.style("\nFAILED", fg="red") + " with status code 422:")
    click.echo("Due to licensing restrictions, you can only access US equity data from Tradologics servers (tradelets, research, etc)")


def single(options):
    identifier = options.first("asset").upper()
    start, _ = utils.parse_date(options.first("start"))
    end, _ = utils.parse_date(
        options.first("end", [datetime.now().strftime("%Y-%m-%d")]))

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

