import pytest
import importlib_resources as pkg_resources
import json
from io import StringIO


@pytest.fixture
def minifam_desired():
    import deciphon as dcp

    txt = pkg_resources.read_text(dcp.test, "minifam_desired.json")
    return json.loads(txt)


@pytest.fixture
def minifam_consensus():
    import deciphon as dcp
    import fasta_reader as fr

    txt = pkg_resources.read_text(dcp.test, "minifam_consensus.fasta")
    return fr.read_fasta(StringIO(txt)).read_items()
