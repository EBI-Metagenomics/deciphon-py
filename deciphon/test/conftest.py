import json
from io import StringIO

import importlib_resources as pkg_resources
import pytest


@pytest.fixture
def minifam_desired():
    import deciphon as dcp

    txt = pkg_resources.read_text(dcp.test, "minifam_desired.json")
    return json.loads(txt)


@pytest.fixture
def minifam_consensus():
    import fasta_reader as fr

    import deciphon as dcp

    txt = pkg_resources.read_text(dcp.test, "minifam_consensus.fasta")
    return fr.read_fasta(StringIO(txt)).read_items()
