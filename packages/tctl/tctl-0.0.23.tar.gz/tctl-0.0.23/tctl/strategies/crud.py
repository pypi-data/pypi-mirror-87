#!/usr/bin/env python

import click
import re
import sys
from .. import utils
from .. import inputs
from .. import remote


import pandas as pd
pd.options.display.float_format = '{:,}'.format

regex = re.compile(
    r'^https?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def strategies_list(options):
    data, errors = remote.api.get("/strategies")
    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo strategies found.")
        return

    click.echo(utils.to_table(data, hide=["url"]))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def strategy_info(options):
    data, errors = remote.api.get("/strategy/{strategy}".format(
        strategy=options.first("strategy")))

    if data.get("as_tradelet", True):
        del data["url"]

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo strategies found.")
        return

    df = pd.DataFrame([data])
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def strategy_status(options):
    data, errors = remote.api.get("/strategy/{strategy}/status".format(
        strategy=options.first("strategy")))

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    click.echo("\nStatus: {status}".format(status=data["status"]))


def strategy_log(options):
    data, errors = remote.api.get("/strategy/{strategy}/logs".format(
        strategy=options.first("strategy")))

    lines = options.get("lines", [10])
    data["logs"] = data["logs"][-abs(int(lines[0])):]

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    if not data["logs"]:
        click.echo("\n[no logs]")
        return
    click.echo("\n" + "\n".join(data["logs"]))


def strategy_update(options):

    strategy, errors = remote.api.get("/strategy/{strategy}".format(
        strategy=options.first("strategy")))

    click.echo()
    name = inputs.text(f"Name [{strategy['name']}]")
    description = inputs.text(f"Description [{strategy['description']}]")
    mode = inputs.option_selector(
        f"Mode [{strategy['mode']}]", ["Backtest", "Paper", "Broker"])

    data, errors = remote.api.patch(
        "/strategy/{strategy}".format(strategy=options.first("strategy")),
        json={
            "name": name,
            "description": description,
            "mode": mode.lower()
        })

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The strategy `{name}` was updated")

    df = pd.DataFrame([data])
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def strategy_delete(options):
    strategy = options.first("strategy")
    remote.api.delete("/strategy/{strategy}".format(strategy=strategy))

    utils.success_response(
        f"The strategy `{strategy}` was removed from your account")


def strategy_set_mode(options):

    strategy, errors = remote.api.get("/strategy/{strategy}".format(
        strategy=options.first("strategy")))

    mode = options.first("mode")

    if mode not in ["backtest", "paper", "broker"]:
        click.echo("\nCurrent mode: {mode}".format(mode=strategy["mode"]))
        click.echo()
        mode = inputs.option_selector(
            "New mode", [strategy["mode"].title()] + [
                mode.title() for mode in [
                    "backtest", "paper", "broker"
                ] if mode != strategy["mode"]
            ])

    if mode.lower() == strategy["mode"]:
        click.echo(f"Aborted! The strategy mode was unchanged ({mode}).")
        return

    data, errors = remote.api.patch(
        "/strategy/{strategy}".format(strategy=options.first("strategy")),
        json={
            "mode": mode.lower()
        })

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The strategy's mode was chaned to `{mode}`")


def strategy_start(options):
    strategy = options.first("strategy")

    data, errors = remote.api.get("/strategy/{strategy}".format(
        strategy=options.first("strategy")))

    if data.get("status") == "Running":
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo(f"The strategy '{strategy}' is already running in {data.get('mode')} mode.")
        sys.exit()

    click.echo(click.style("\n>>> NOTE:  ", fg="yellow"), nl=False)
    click.echo("""Strategies running in Paper mode needs to have
a dedicated \"paper\" account associated with them in order
to calculate strategy's performance and determine its
capabilities (such as start balance and shorting/margin).
""")

    payload = utils.virtual_account_payload(data.get("mode"))

    data, errors = remote.api.post(f"/strategy/{strategy}/start", json=payload)

    if "Tradelet" in data["message"]:
        data["message"] = [
            "Tradelet deploy initialized...\n",
            f"  - Check status using `tctl strategies status --strategy {strategy}`",
            f"  - Deploy log is available via `tctl strategies log --strategy {strategy}`",
        ]
    else:
        data["message"] = ["Strategy starting.."]

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response("\n".join(data["message"]))


def strategy_stop(options, _response=True):
    strategy = options.first("strategy")
    remote.api.post(
        "/strategy/{strategy}/stop".format(strategy=strategy))

    if _response:
        utils.success_response(f"The strategy `{strategy}` was stopped.")


def strategy_create(options):
    click.echo()
    name = ""
    while name == "":
        name = inputs.text("Strategy name")
    description = inputs.text("Description (leave blank for none)")
    mode = inputs.option_selector(
        "Mode", ["Backtest", "Paper", "Broker"])

    as_tradelet = inputs.confirm(
        "Run strategy on Tradologics (via Tradelets)?", default=True)
    url = None
    if not as_tradelet:
        while url is None:
            url = inputs.text(
                "Strategy URL", validate=lambda _, x: re.match(regex, x))

    payload = {
        "name": name,
        "description": description,
        "mode": mode.lower(),
        "as_tradelet": as_tradelet,
    }
    if url:
        payload["url"] = url

    data, errors = remote.api.post("/strategies", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The strategy `{name}` ({mode}) was added to your account.")

    cols = ['name', 'strategy_id', 'description', 'as_tradelet', 'mode']
    if not as_tradelet:
        cols.append("url")
    df = pd.DataFrame([data])[cols]
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def strategy_stats(options):
    error = {
        "id": "unprocessable_request",
        "message": "Not supported yet via tctl"
    }
    click.echo(click.style("\nFAILED", fg="red"), nl=False)
    click.echo(" (status code 422):")
    click.echo(utils.to_json(error))

