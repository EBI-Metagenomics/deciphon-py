from pathlib import Path

from blx.cid import CID
from blx.progress import Progress


def sha256sum(filepath: Path):
    return CID.from_file(filepath, progress=Progress("Hash")).hex()
