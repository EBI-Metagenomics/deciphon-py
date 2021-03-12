import logging
from pathlib import Path

import pooch

__all__ = ["get"]

pooch.get_logger().setLevel(logging.ERROR)


registry = {
    "minifam.hmm.gz": "md5:2f0d22cec2ae29af4755913652d205d4",
    "pfam24.hmm.gz": "md5:e927fd1fc25bd56d8f70a3fa97223304",
}

goodboy = pooch.create(
    path=pooch.os_cache("deciphon"),
    base_url="https://deciphon.s3.amazonaws.com/",
    registry=registry,
)


def get(filename: str) -> Path:
    return Path(
        goodboy.fetch(filename + ".gz", processor=pooch.Decompress(name=filename))
    )
