from pathlib import Path

from blx.cid import CID
from blx.client import get_client as get_blx
from blx.progress import Progress

__all__ = ["storage_has", "storage_put", "storage_get"]


def storage_has(cid: CID) -> bool:
    return get_blx().has(cid)


def storage_put(cid: CID, filepath: Path):
    return get_blx().put(cid, filepath, progress=Progress("Upload"))


def storage_get(cid: CID, filepath: Path):
    return get_blx().get(cid, filepath, progress=Progress("Download"))
