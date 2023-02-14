from __future__ import annotations

import asyncio
import importlib.metadata
from pathlib import Path
from typing import Optional

import typer
from deciphon_core.press import Press
from deciphon_core.h3result import H3Result
from rich.progress import track

import deciphon.cli_api
import deciphon.pressd
import deciphon.scan
import deciphon.scand
from deciphon.service_exit import ServiceExit, register_service_exit

__all__ = ["app"]


app = typer.Typer(
    add_completion=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)

PROGRESS_OPTION = typer.Option(
    True, "--progress/--no-progress", help="Display progress bar."
)


@app.callback(invoke_without_command=True)
def cli(version: Optional[bool] = typer.Option(None, "--version", is_eager=True)):
    if version:
        typer.echo(importlib.metadata.version(__package__))
        raise typer.Exit()


@app.command()
def press(hmm: Path, progress: bool = PROGRESS_OPTION):
    """
    Press HMM ASCII file into a Deciphon database one.
    """
    register_service_exit()

    db = Path(hmm.stem + ".dcp")
    try:
        with Press(hmm, db) as press:
            for _ in track(press, "Press", disable=not progress):
                pass
    except ServiceExit:
        raise typer.Exit(1)


@app.command()
def scan(
    hmm: Path,
    seq: Path,
    progress: bool = PROGRESS_OPTION,
    force: bool = typer.Option(
        False, "--force", help="Remove output directory if necessary."
    ),
):
    """
    Annotate nucleotide sequences into proteins a protein database.
    """
    register_service_exit()
    del progress

    try:
        deciphon.scan.scan(hmm, seq, force)
    except ServiceExit:
        raise typer.Exit(1)


@app.command()
def see(snap: Path):
    """
    Display scan results stored in a snap file.
    """
    register_service_exit()

    try:
        h3r = H3Result(snap)
        stream = typer.get_text_stream("stdout")
        h3r.print_targets(stream)
        h3r.print_targets_table(stream)
        h3r.print_domains(stream)
        h3r.print_domains_table(stream)
    except ServiceExit:
        raise typer.Exit(1)


@app.command()
def start(daemon: str):
    """
    Start `pressd` or `scand` daemons.
    """
    register_service_exit()

    if daemon == "pressd":
        asyncio.run(deciphon.pressd.pressd())
    if daemon == "scand":
        asyncio.run(deciphon.scand.scand())


app.add_typer(deciphon.cli_api.app, name="api")
