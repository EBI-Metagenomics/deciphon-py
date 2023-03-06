from __future__ import annotations

import importlib.metadata
from pathlib import Path
from typing import Optional

from deciphon_core.h3result import H3Result
from rich.progress import track
from typer import Exit, Option, Typer, echo, get_text_stream

from deciphon.h3daemon import H3Daemon
from deciphon.hmmer_press import hmmer_press
from deciphon.hmmfile import HMMFile
from deciphon.press import Press
from deciphon.snapfile import NewSnapFile
from deciphon.scan import Scan
from deciphon.seqfile import SeqFile
from deciphon.service_exit import service_exit

__all__ = ["app"]


app = Typer(
    add_completion=False,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)

O_PROGRESS = Option(True, "--progress/--no-progress", help="Display progress bar.")


@app.callback(invoke_without_command=True)
def cli(version: Optional[bool] = Option(None, "--version", is_eager=True)):
    if version:
        echo(importlib.metadata.version(__package__))
        raise Exit(0)


@app.command()
def press(hmm: Path, progress: bool = O_PROGRESS):
    """
    Press HMM file.
    """
    with service_exit():
        hmmfile = HMMFile(path=hmm)
        with Press(hmmfile) as press:
            for x in track(press, "Pressing", disable=not progress):
                x.press()
            hmmer_press(hmmfile.path)


@app.command()
def scan(hmm: Path, seq: Path, snap: Optional[Path] = None):
    """
    Scan nucleotide sequences.
    """
    with service_exit():
        hmmfile = HMMFile(path=hmm)

        if not snap:
            snapfile = NewSnapFile(path=seq.parent / f"{seq.stem}.dcs")
        else:
            snapfile = NewSnapFile(path=snap)

        with SeqFile(seq) as seqfile:
            with H3Daemon(hmmfile) as daemon:
                scan = Scan(hmmfile, seqfile, snapfile)
                scan.port = daemon.port
                with scan:
                    scan.run()


@app.command()
def see(snap: Path):
    """
    Display scan results stored in a snap file.
    """
    with service_exit():
        h3r = H3Result(snap)
        stream = get_text_stream("stdout")
        h3r.print_targets(stream)
        h3r.print_targets_table(stream)
        h3r.print_domains(stream)
        h3r.print_domains_table(stream)
