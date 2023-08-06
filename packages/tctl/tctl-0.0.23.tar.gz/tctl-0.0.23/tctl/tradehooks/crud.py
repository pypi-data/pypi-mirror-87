#!/usr/bin/env python

import click
from .. import utils
from .. import inputs
from .. import remote
from ..strategies.crud import strategy_stop
import ujson as json
import yaml
import sys
from pathlib import Path

import pandas as pd
pd.options.display.float_format = '{:,}'.format


def format_offset(offset):
    offset = str(offset).replace("+", "")
    try:
        offset = int(offset)
        if offset > 0:
            return f'open + {offset}min'
        elif offset < 0:
            return f'open{offset}min'.replace("-", " - ")
        else:
            return 'open'
    except Exception:
        pass
    return offset


def tradehooks_list(options):
    data, errors = remote.api.get("/tradehooks")

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo Tradehooks found.")
        return

    table_data = []
    for item in data:
        schedule = item.get("rule", {}).get("schedule", {})
        o = format_offset(schedule.get("session", {}).get("open"))
        c = format_offset(schedule.get("session", {}).get("close"))

        on_days = schedule.get("on_days", "*")
        if isinstance(on_days, list):
            on_days = ", ".join(schedule.get("on_days"))

        table_data.append({
            # "name": item["tradehook"],
            "tradehook_id": item["tradehook_id"],
            "comment": item["comment"],
            "strategies": len(item["strategies"]),
            # "assets": len(item["assets"]),
            "invocations": "{:,.0f}".format(item["invocations"]),
            "days": on_days.title(),
            "session": f'{schedule.get("exchange")}: {o} to {c}',
            "timing": schedule.get("timing"),
        })
    click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def tradehook_info(options):
    data, errors = remote.api.get("/tradehook/{tradehook}".format(
        tradehook=options.first("tradehook")))

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    schedule = data.get("rule", {}).get("schedule", {})
    o = format_offset(schedule.get("session", {}).get("open"))
    c = format_offset(schedule.get("session", {}).get("close"))

    data = {
        "name": data["tradehook"],
        "tradehook_id": data["tradehook_id"],
        "comment": data["comment"],
        "strategies": len(data["strategies"]),
        # "assets": len(data["assets"]),
        "invocations": "{:,.0f}".format(data["invocations"]),
        "days": ", ".join(schedule.get("on_days")).title(),
        "session": f'{schedule.get("exchange")}: {o} to {c}',
        "timing": schedule.get("timing"),
    }

    df = pd.DataFrame([data])
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def tradehook_create(options, from_update=False):
    strategies = {}
    supported_strategies, errors = remote.api.get("/strategies")
    for strategy in supported_strategies:
        strategies[strategy['name']] = strategy["strategy_id"]

    click.echo("")
    name = ""
    if from_update:
        name = inputs.text("Tradehook name [{s}]".format(
            s=options.first("tradehook")))
    else:
        while name == "":
            name = inputs.text("Tradehook name")

    config_file_found = False
    while not config_file_found:
        config_file = inputs.path(
            "Path to Tradehook configuration file", validator="file")
        config_file_found = Path(config_file).exists()

    selected_strategies = inputs.checkboxes(
        "Attach to strategy/ies (optional, can be done later)", list(
            strategies.keys()))

    # if not selected_strategies:
    #     click.echo(click.style("\nFAILED", fg="red"))
    #     click.echo("Tradehook *must* be associated with at least one strategy.")

    strategies = [s for n, s in strategies.items() if n in selected_strategies]

    payload = {}
    if ".json" in config_file:
        with open(Path(config_file), encoding="utf-8") as f:
            try:
                payload = json.load(f)
            except ValueError:
                click.echo(click.style("\nFAILED", fg="red"))
                click.echo("Cannot parse JSON. Is this a valid JSON file?")
                sys.exit()
    else:
        with open(Path(config_file), encoding="utf-8") as f:
            try:
                payload = yaml.load(f, Loader=yaml.SafeLoader)
            except yaml.parser.ParserError:
                click.echo(click.style("\nFAILED", fg="red"))
                click.echo("Cannot parse YAML. Is this a valid YAML file?")
                sys.exit()

    if not payload:
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo("Tradehook configuration file appears to be empty.")

    if strategies:
        payload["strategies"] = strategies
    payload["name"] = name
    payload["comment"] = inputs.text("Comment (optional)")

    if from_update:
        return payload
    data, errors = remote.api.post("/tradehooks", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The Tradehook `{name}` was added to your account.")
    if strategies:
        click.echo("It was attached to:")
        click.echo("  - "+"\n  - ".join(strategies))


def tradehook_update(options):
    name = options.first("tradehook")

    payload = tradehook_create(options, from_update=True)
    if payload["name"] == "":
        tradehook, errors = remote.api.get("/tradehook/{tradehook}".format(
            tradehook=options.first("tradehook")))
        payload["name"] = tradehook["tradehook"]

    data, errors = remote.api.patch(
        f"/tradehook/{name}", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The tradehook `{name}` was updated successfully. It's now attached to:")
    click.echo("  - "+"\n  - ".join(payload["strategies"]))


def tradehook_attach(options):
    tradehook = options.first("tradehook")
    data, errors = remote.api.get("/tradehook/{tradehook}".format(
        tradehook=tradehook))

    payload = {
        "name": data["tradehook"],
        "comment": data["comment"],
        "strategies": data["strategies"],
        "when": {
            "schedule": data["rule"]["schedule"]
        },
        "what": {
            "assets": data["assets"],
            "bar": data["lookback_resolution"],
            "history": data["lookback_history"]
        }
    }

    strategy = options.get("strategy")
    if strategy:
        strategy = strategy[0]
        payload["strategies"].append(strategy)
    else:
        strategies = {}
        supported_strategies, errors = remote.api.get("/strategies")
        for strategy in supported_strategies:
            strategies[strategy['name']] = strategy["strategy_id"]

        selected_strategies = inputs.checkboxes(
            "Attach to strategy(ies)", list(strategies.keys()))

        for n, s in strategies.items():
            if n in selected_strategies:
                data["strategies"].append(s)

    payload["strategies"] = list(set(data["strategies"]))

    if not payload["strategies"]:
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo("Select at least one strategy.")

    data, errors = remote.api.patch(
        f"/tradehook/{tradehook}/strategies", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The tradehook account `{tradehook}` was successfully attached to:")
    click.echo("  - "+"\n  - ".join(payload["strategies"]))


def tradehook_detach(options):
    tradehook = options.first("tradehook")
    data, errors = remote.api.get("/tradehook/{tradehook}".format(
        tradehook=tradehook))

    click.echo("")
    if not data.get("strategies", []):
        click.echo("\nThis Tradehook isn't attached to any strategies. Nothing to detach...")
        sys.exit(0)

    payload = {
        "name": data["tradehook"],
        "comment": data["comment"],
        "strategies": data["strategies"],
        "when": {
            "schedule": data["rule"]["schedule"]
        },
        "what": {
            "assets": data["assets"],
            "bar": data["lookback_resolution"],
            "history": data["lookback_history"]
        }
    }

    strategy = options.first("strategy")
    if strategy:
        if strategy not in payload["strategies"]:
            click.echo(f"This Tradehook `{tradehook}` isn't attached to strategy `{strategy}`")
            sys.exit(0)
        payload["strategies"].remove(strategy)

        # # check remaining tradehook for strategy
        # if tradehook_count == 0:
        #     strategy_stop(utils.dictx({
        #         "strategy": [strategy],
        #         "raw": options.get("raw", False)
        #         }), _response=False)
        #     click.echo(f"Stopping strategy: `{strategy}`...")

    else:
        strategies = {}
        supported_strategies, errors = remote.api.get("/strategies")
        for strategy in supported_strategies:
            if strategy["strategy_id"] in payload["strategies"]:
                strategies[strategy['name']] = strategy["strategy_id"]

        selected_strategies = inputs.checkboxes(
            "Detach from strategy(ies)", list(strategies.keys()))

        if not selected_strategies:
            click.echo(click.style("\nAborted!", fg="red"))
            click.echo("At least one strategy needs to be selected.")
            sys.exit(0)

        for s in selected_strategies:
            data["strategies"].remove(strategies[s])
            # # check remaining tradehook for strategy
            # if tradehook_count == 0:
            #     strategy_stop(utils.dictx({
            #         "strategy": [strategies[s]],
            #         "raw": options.get("raw", False)
            #     }), _response=False)
            #     click.echo(f"Stopping strategy: `{strategies[s]}`...")

    data, errors = remote.api.patch(
        f"/tradehook/{tradehook}/strategies", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"\nThe tradehook account `{tradehook}` is now attached to:")
    click.echo("  - "+"\n  - ".join(payload["strategies"]))


def tradehook_delete(options):
    tradehook = options.first("tradehook")
    remote.api.delete("/tradehook/{tradehook}".format(
        tradehook=options.first("tradehook")))

    utils.success_response(
        f"The tradehook `{tradehook}` was removed from your account")
