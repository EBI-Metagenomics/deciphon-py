from __future__ import annotations

import asyncio
import importlib.metadata
from pathlib import Path
from typing import Optional

import typer
from deciphon_core.h3result import H3Result
from typer import Exit, Option, Typer, echo

import deciphon.cli_api
import deciphon.pressd
import deciphon.scand
from deciphon.hmmfile import HMMFile
from deciphon.prodfile import ProdFile
from deciphon.seqfile import SeqFile
from deciphon.press import Press
from deciphon.scan import Scan
from deciphon.service_exit import service_exit
from h3daemon.sched import SchedContext
from rich.progress import track

__all__ = ["app"]


app = Typer(
    add_completion=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)

O_PROGRESS = Option(True, "--progress/--no-progress", help="Display progress bar.")
O_FORCE = Option(False, "--force")


@app.callback(invoke_without_command=True)
def cli(version: Optional[bool] = Option(None, "--version", is_eager=True)):
    if version:
        echo(importlib.metadata.version(__package__))
        raise Exit(0)


@app.command()
def press(hmm: Path, force: bool = O_FORCE, progress: bool = O_PROGRESS):
    """
    Press HMM file.
    """
    with service_exit():
        hmmfile = HMMFile(hmm)
        if force:
            hmmfile.dbfile.unlink(True)
        elif hmmfile.dbfile.exists():
            raise RuntimeError(f"{hmmfile.dbfile} already exists.")

        with Press(hmmfile) as press:
            for x in track(press, "Pressing", disable=not progress):
                x.press()


@app.command()
def scan(
    hmm: Path,
    seq: Path,
    prod: Optional[Path] = None,
    force: bool = O_FORCE,
):
    """
    Scan nucleotide sequences.
    """
    with service_exit():
        hmmfile = HMMFile(hmm)
        if not hmmfile.dbfile.exists():
            raise FileNotFoundError(f"{hmmfile.dbfile} does not exist.")

        seqfile = SeqFile(seq)
        prodfile = ProdFile(prod) if prod else ProdFile.from_seqfile(seqfile)

        h3file = hmmfile.h3file
        h3file.ensure_pressed()

        if force:
            prodfile.remove_all(True)
        elif prodfile.path.exists():
            raise RuntimeError(f"{prodfile.path} already exists.")
        elif prodfile.basedir.exists():
            raise RuntimeError(f"{prodfile.basedir} already exists.")

        with SchedContext(hmmfile.h3file) as sched:
            sched.is_ready(wait=True)
            scan = Scan(hmmfile, seqfile, prodfile)
            scan.port = sched.master.get_port()
            with scan:
                scan.run()


@app.command()
def see(snap: Path):
    """
    Display scan results stored in a snap file.
    """
    with service_exit():
        h3r = H3Result(snap)
        stream = typer.get_text_stream("stdout")
        h3r.print_targets(stream)
        h3r.print_targets_table(stream)
        h3r.print_domains(stream)
        h3r.print_domains_table(stream)


@app.command()
def start(daemon: str):
    """
    Start `pressd` or `scand` daemons.
    """
    with service_exit():
        if daemon == "pressd":
            asyncio.run(deciphon.pressd.pressd())
        if daemon == "scand":
            asyncio.run(deciphon.scand.scand())


app.add_typer(deciphon.cli_api.app, name="api")
