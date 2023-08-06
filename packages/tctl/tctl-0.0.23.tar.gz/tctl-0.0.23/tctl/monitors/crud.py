#!/usr/bin/env python

import click
# import ujson
from .. import utils
from .. import inputs
from .. import remote
from decimal import Decimal
import re
import pandas as pd
pd.options.display.float_format = '{:,}'.format


def monitors_list(options):
    strategy = options.first("strategy")
    data, errors = remote.api.get(f"/monitor/{strategy}")

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo monitors found.")
        return

    table_data = []
    for item in data:
        table_data.append({
            "id": item["id"],
            "asset": item["asset"],
            "rule": item["rule"].replace("_", " ").title().replace(" Or ", " or "),
            "price": "{:,.2f}".format(Decimal(item["price"])),
            "strategies": len(item["strategies"])
        })
    click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def monitor_create(options):
    strategies = {}
    supported_strategies, errors = remote.api.get("/strategies")
    for strategy in supported_strategies:
        strategies[strategy['name']] = strategy["strategy_id"]

    click.echo("")

    if options.first("type") not in ["price", "position"]:
        kind = inputs.option_selector(
            "Monitor type", ["Price", "Position"]).lower()

    asset = ""
    while asset == "":
        asset = inputs.text("Asset to monitor")

    rule = inputs.option_selector(
        "Condition",
        ["Above", "Above or Equal", "Below", "Below or Equal"]
    ).lower().replace(" ", "_")

    if kind == "price":
        account = ""
        num = inputs.text(
            "Target price",
            validate=lambda _, x: re.match(re.compile(r'(\d+(\.\d+)?)'), x))

    elif kind == "position":
        num = inputs.text(
            "Target Percent",
            validate=lambda _, x: re.match(re.compile(r'(0+(\.\d+)?)'), x))

        accounts = {}
        supported_accounts, errors = remote.api.get("/accounts")
        for key, account in supported_accounts.items():
            accounts[account['name']] = account["account_id"]
        account = accounts[inputs.option_selector(
            "Broker account", list(accounts.keys()))]

    selected_strategies = inputs.checkboxes(
        "Motify strategy(ies)", list(strategies.keys()))

    if not selected_strategies:
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo("Tradehook *must* be associated with at least one strategy.")

    strategies = [s for n, s in strategies.items() if n in selected_strategies]

    payload = {
        "strategies": strategies,
        "asset": asset,
        "rule": rule,
    }
    if kind == "price":
        payload["price"] = float(num)
    else:
        payload["account"] = account
        payload["pct"] = float(num)

    # click.echo(utils.to_json(payload))
    data, errors = remote.api.post(f"/monitor/{kind}", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The monitor was created with the id `{data['id']}`.")
    click.echo("\nThe following strategies will be notified:")
    click.echo("  - "+"\n  - ".join(data["strategies"]))


def monitor_delete(options):
    monitor = options.first("monitor")
    remote.api.delete("/monitor/{monitor}".format(
        monitor=options.first("monitor")))

    utils.success_response(
        f"The monitor `{monitor}` was removed from your account")
