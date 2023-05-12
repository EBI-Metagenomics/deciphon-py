import os
from pathlib import Path

from blx import BLXApp
from blx.cid import CID

from deciphon.hmmfile import HMMFile
from deciphon.press import Press

cid = CID(sha256hex="fe305d9c09e123f987f49b9056e34c374e085d8831f815cc73d8ea4cdec84960")


def test_press(tmp_path: Path):
    os.chdir(tmp_path)
    BLXApp().get(cid, "minifam.hmm")
    hmmfile = HMMFile(path=Path("minifam.hmm"))
    with Press(hmmfile) as press:
        for x in press:
            x.press()
    db = hmmfile.dbfile
    assert db.path.stat().st_size == 9933912
