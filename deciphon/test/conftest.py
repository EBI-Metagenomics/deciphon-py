import pytest
import importlib_resources as pkg_resources
import json


@pytest.fixture
def minifam_desired():
    import deciphon as dcp

    txt = pkg_resources.read_text(dcp.test, "minifam_desired.json")
    return json.loads(txt)
