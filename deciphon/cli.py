from __future__ import annotations

import importlib.metadata
from pathlib import Path
from typing import Optional

import typer
from rich.progress import track

from deciphon_core.press import Press
import deciphon.scan
from deciphon.service_exit import ServiceExit, register_service_exit

__all__ = ["app"]


app = typer.Typer(add_completion=False)

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
