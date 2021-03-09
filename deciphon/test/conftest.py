import json
from io import StringIO

import fasta_reader as fr
import importlib_resources as pkg_resources
import pytest


@pytest.fixture
def minifam():
    import deciphon as dcp

    fasta = pkg_resources.read_text(dcp.test, "minifam.fasta")
    desired = pkg_resources.read_text(dcp.test, "minifam.json")

    return {
        "hmm": dcp.example.get("minifam.hmm"),
        "targets": fr.read_fasta(StringIO(fasta)).read_items(),
        "desired": json.loads(desired),
    }


@pytest.fixture
def pfam24():
    import deciphon as dcp

    fasta = pkg_resources.read_text(dcp.test, "AE014075.1.fasta")
    desired = pkg_resources.read_text(dcp.test, "pfam24_AE014075.json")

    return {
        "hmm": dcp.example.get("Pfam-A_24.hmm"),
        "targets": fr.read_fasta(StringIO(fasta)).read_items(),
        "desired": json.loads(desired),
    }
