#!/usr/bin/env python

import click
# import ujson
from .. import utils
from .. import remote
from decimal import Decimal
import pandas as pd
pd.options.display.float_format = '{:,}'.format


def positions_list(options):

    account = options.first("account")
    # accounts_data, errors = remote.api.get("/accounts")
    # accounts = {k: v["name"] for k, v in accounts_data.items()}
    # if account not in accounts:
    #     click.echo(f"Account `{account}` doesn't exist or was deleted.")
    #     return

    endpoint = "/positions"
    payload = {}

    if account:
        endpoint = "/account/{account}/positions".format(account=account)
    if options.get("strategy"):
        payload["strategies"] = options.get("strategy")
    if options.get("start"):
        payload["date_from"] = options.get("start")
    if options.get("end"):
        payload["date_to"] = options.get("end")
    if options.get("status"):
        payload["statuses"] = options.get("status")

    if payload:
        data, errors = remote.api.get(endpoint, json=payload)
    else:
        data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo positions found.")
        return

    table_data = []

    if not account:
        # display count
        for act, positions in data.items():
            table_data.append({
                "account": act,  # accounts.get(act, act),
                "positions": len(positions)
            })
    else:
        # display  order list
        if not data.get(account):
            click.echo("\nNo positions found for account {}".format(account))
            return

        for item in data.get(account):
            table_data.append({
                "id": item["order_id"],
                "asset": item["ticker"],
                "side": item["side"],
                "qty": "{:,.0f}".format(Decimal(item["qty"])),
                "filled_qty": "{:,.0f}".format(Decimal(item["filled_qty"])),
                "avg_fill_price": item["avg_fill_price"],
                "status": item["status"]
            })
    click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def trades_list(options):

    account = options.first("account")
    # accounts_data, errors = remote.api.get("/accounts")
    # accounts = {k: v["name"] for k, v in accounts_data.items()}
    # if account not in accounts:
    #     click.echo(f"Account `{account}` doesn't exist or was deleted.")
    #     return

    endpoint = "/trades"
    payload = {}

    if account:
        endpoint = "/account/{account}/trades".format(account=account)
    if options.get("strategy"):
        payload["strategies"] = options.get("strategy")
    if options.get("start"):
        payload["date_from"] = options.get("start")
    if options.get("end"):
        payload["date_to"] = options.get("end")
    if options.get("status"):
        payload["statuses"] = options.get("status")

    if payload:
        data, errors = remote.api.get(endpoint, json=payload)
    else:
        data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo trades found.")
        return

    table_data = []

    if not account:
        # display count
        for act, trades in data.items():
            table_data.append({
                "account": act,  # accounts.get(act, act),
                "trades": len(trades)
            })
    else:
        # display  order list
        if not data.get(account):
            click.echo("\nNo trades found for account {}".format(account))
            return

        for item in data.get(account):
            table_data.append({
                "id": item["order_id"],
                "asset": item["ticker"],
                "side": item["side"],
                "qty": "{:,.0f}".format(Decimal(item["qty"])),
                "filled_qty": "{:,.0f}".format(Decimal(item["filled_qty"])),
                "avg_fill_price": item["avg_fill_price"],
                "status": item["status"]
            })
    click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


