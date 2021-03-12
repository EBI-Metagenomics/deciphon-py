import gzip
import json
from io import StringIO

import fasta_reader as fr
import importlib_resources as pkg_resources
import pytest

import deciphon as dcp


def get_data(filename: str):

    fasta_gz = pkg_resources.read_binary(dcp.test, f"{filename}.fasta.gz")
    fasta = gzip.decompress(fasta_gz).decode()

    json_gz = pkg_resources.read_binary(dcp.test, f"{filename}.json.gz")
    data = json.loads(gzip.decompress(json_gz))

    desired = {}
    for d in data:
        key = (d["multiple_hits"], d["hmmer3_compat"], d["target"], d["profile"])
        desired[key] = {
            "alt_loglik": d["alt_loglik"],
            "alt_path": d["alt_path"],
            "alt_codon_stream": d["alt_codon_stream"],
            "null_loglik": d["null_loglik"],
            "null_path": d["null_path"],
            "null_codon_stream": d["null_codon_stream"],
        }

    return {
        "hmm": dcp.example.get(f"{filename}.hmm"),
        "targets": fr.read_fasta(StringIO(fasta)).read_items(),
        "desired": desired,
    }


@pytest.fixture
def minifam():
    return get_data("minifam")


@pytest.fixture
def pfam24():
    return get_data("pfam24")
