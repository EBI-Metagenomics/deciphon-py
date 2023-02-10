from typing import List

from pydantic import BaseModel


class HMM(BaseModel):
    id: int
    filename: str
    sha256: str
    job_id: int


class HMMCreate(BaseModel):
    sha256: str
    filename: str


class DBCreate(BaseModel):
    sha256: str
    filename: str


class SeqCreate(BaseModel):
    name: str
    data: str


class ScanCreate(BaseModel):
    multi_hits: bool
    hmmer3_compat: bool
    db_id: int
    seqs: List[SeqCreate]
