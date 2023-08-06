import os
import pathlib
import subprocess
from pathlib import Path

import typer

from datajob.package import wheel
from datajob import logger

app = typer.Typer()
filepath = pathlib.Path(__file__).resolve().parent


def run():
    """entrypoint for datajob"""
    app()


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def deploy(
        config: str = typer.Option(Path, callback=os.path.abspath),
        package: bool = typer.Option(False, "--package"),
        ctx: typer.Context = typer.Option(list),
):
    if package:
        project_root = str(Path(config).parent)
        wheel.create(project_root=project_root)
    # create stepfunctions if requested
    args = ["--app", f"'python {config}'"]
    extra_args = ctx.args
    call_cdk(command="deploy", args=args, extra_args=extra_args)


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def orchestrate(config: str = typer.Option(...)):
    pass


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def destroy(config: str = typer.Option(...)):
    call_cdk(command="destroy", args=" ".join(["--app", f"python {config}"]))


def call_cdk(command: str, args: list = None, extra_args: list = None):
    args = args if args else []
    extra_args = extra_args if extra_args else []
    full_command = " ".join(["cdk", command] + args + extra_args)
    print(f"cdk command {full_command}")
    subprocess.call(full_command, shell=True)
