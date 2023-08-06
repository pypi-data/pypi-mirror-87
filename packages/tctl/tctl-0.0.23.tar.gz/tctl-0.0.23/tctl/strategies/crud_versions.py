
import click
import sys
import ujson
from base64 import b64encode as _b64encode
from pathlib import Path
from .. import utils
from .. import inputs
from .. import remote

import pandas as pd
pd.options.display.float_format = '{:,}'.format


STRATEGY_FILES = {
    "python2": "strategy.py",
    "python3": "strategy.py",
    "node": "strategy.js",
    "php": "strategy.php",
    "go": "strategy.go",
    "ruby": "strategy.rb",
    "java11": "strategy.java",
    "java8": "strategy.java",
    "csharp": "strategy.cs"
}

LANGUAGES = [
    "Python 3",
    "Python 2",
    "Node",
    "Go",
    "C-Sharp",
    "PHP",
    "Ruby",
    "Java 8",
    "Java 11"
]
LANGUAGE_KEYS = [
    l.replace(" ", "").replace("-", "").lower() for l in LANGUAGES
]


def strategy_deploy(options):
    strategy = options.first("strategy")
    remote.api.get("/strategy/{strategy}".format(
        strategy=strategy))

    click.echo("")

    lang = options.get("lang")
    show_lang_selector = (lang is None) or (
        isinstance(lang, list) and
        lang[0] in LANGUAGES and
        lang[0] not in ["python3", "python2", "node"])

    if not show_lang_selector:
        lang = lang[0]
    else:
        click.echo("-----------------------------")
        click.echo(click.style("PLEASE NOTE:", fg="red"))
        click.echo(
            "Currently, only Python and Node are supported by the backtester.")
        click.echo("-----------------------------\n")
        lang = inputs.option_selector(
            "Language", LANGUAGES
        ).replace(" ", "").replace("-", "").lower()

    # --- future ---
    # path = inputs.path("Path to code directory", validator="directory")

    # --- now ---
    strategy_file_found = False
    while not strategy_file_found:
        strategy_file = inputs.path(
            "Path to `{file}`".format(file=STRATEGY_FILES[lang]), validator="file")
        strategy_file_found = Path(strategy_file).exists()

    path = Path(strategy_file).parents[0]
    dependencies = []
    if "python" in lang:
        dep_file = 'requirements.txt'
        req_file = path / dep_file
    elif "node" in lang:
        dep_file = 'package.json'
        req_file = path / dep_file

    if req_file and req_file.is_file():
        if inputs.confirm(
                f"Found dependencies file `{dep_file}`. Import it?", default=True):
            dependencies = _read_dependencies(lang, str(path))

    # --- continue ---
    comment = inputs.text("Comment (optional)")
    payload = {
        # "code": _prepare_deploy(lang, path),
        "code": {
            "code": _read_file(strategy_file),
            "dependencies": dependencies,
            "lang": lang
        },
        "comment": comment
    }

    # print(utils.to_json(payload))
    data, errors = remote.api.post(
        "/strategy/{strategy}/versions".format(strategy=strategy),
        json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        """Strategy code (v{version}) was deployed successfully.

NOTE: If you haven't already, attach a Tradehook
to this strategy and start your strategy using:

$ tctl strategies start --strategy {strategy}
        """.format(
            strategy=strategy,
            version=data["version"]
        ))


def _prepare_deploy(lang, directory):
    files = _read_files(directory, STRATEGY_FILES[lang])
    dependencies = _read_dependencies(lang, directory)
    return {
        # "files": files,
        "code": files[STRATEGY_FILES[lang]],
        "dependencies": dependencies,
        "lang": lang
    }


def _read_files(directory, required):
    ignore_list = """
        node_modules
        .git
        __pycache__
        tests
        docs
        examples
        demo
        .sql
        .md
        .DS_Store
        .env
        requirements.txt
        package.json
        .sh
        .loc
        vendor/
        """.strip().split()

    files = {}
    for path in Path(directory).glob("*"):
        if path.is_file():
            include = True
            for ignore in ignore_list:
                if ignore in str(path):
                    include = False
                    break
            if include:
                files[path.name] = _read_file(path)

    if required not in files.keys():
        click.echo(click.style("\nERROR: ", fg="red"), nl=False)
        click.echo("Cannot find a file named `{file}`".format(file=required))
        sys.exit()

    return files


def _read_file(file):
    # import chardet
    # rawdata = open(file).read()
    # encoding = chardet.detect(rawdata).get("encoding", "utf-8")
    with open(file, encoding="utf-8") as f:
        return _b64encode(f.read().encode()).decode()
    return ""


def _read_dependencies(lang, path):
    path = Path(path)
    dependencies = []

    # python
    if "python" in lang:
        req_file = path / 'requirements.txt'
        if req_file.is_file():
            with open(req_file, encoding="utf-8") as f:
                lines = [line.rstrip() for line in f]
                for line in lines:
                    line = line.replace('>', '=').replace(
                        '<', '=').replace('==', '=')
                    package, version = line.split('=')
                    dependencies.append({
                        "package": package,
                        "version": version
                    })
        return dependencies

    # node
    if "node" in lang:
        req_file = path / 'package.json'
        if req_file.is_file():
            with open(req_file, encoding="utf-8") as f:
                lines = ujson.load(f).get('dependencies', [])
                for package, version in lines.items():
                    dependencies.append({
                        "package": package,
                        "version": version.strip('^')
                    })
        return dependencies

    return dependencies
