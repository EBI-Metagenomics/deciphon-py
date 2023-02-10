from __future__ import annotations

from pathlib import Path
from typing import List

import typer
from pydantic import parse_file_as

from deciphon.api import get_api
from deciphon.models import ScanCreate, SeqCreate

app = typer.Typer(add_completion=False)


@app.command()
def create_hmm(hmm: Path):
    get_api().create_hmm(hmm)


@app.command()
def read_hmm(hmm_id: int):
    print(get_api().read_hmm(hmm_id))


@app.command()
def read_hmms():
    print(get_api().read_hmms())


@app.command()
def create_db(db: Path):
    get_api().create_db(db)


@app.command()
def read_db(db_id: int):
    print(get_api().read_db(db_id))


@app.command()
def read_dbs():
    print(get_api().read_dbs())


@app.command()
def create_scan(db_id: int, seqs: Path):
    x = parse_file_as(List[SeqCreate], seqs, content_type="json")
    scan = ScanCreate(db_id=db_id, seqs=x, multi_hits=True, hmmer3_compat=False)
    get_api().create_scan(scan)


@app.command()
def read_scan(scan_id: int):
    print(get_api().read_scan(scan_id))


@app.command()
def read_scans():
    print(get_api().read_scans())


@app.command()
def read_job(job_id: int):
    print(get_api().read_job(job_id))


@app.command()
def read_jobs():
    print(get_api().read_jobs())
