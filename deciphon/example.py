import logging
from pathlib import Path

import pooch

__all__ = ["get"]

pooch.get_logger().setLevel(logging.ERROR)

registry = {
    "minifam.hmm.gz": "md5:be34be2c5bcadcf670031c789b91674b",
    "Pfam-A_24.hmm.gz": "md5:1728570f2d8aba5b140e9ff4071fb0f9",
}

goodboy = pooch.create(
    path=pooch.os_cache("deciphon"),
    base_url="https://iseq-py.s3.amazonaws.com/",
    registry=registry,
)


def get(filename: str) -> Path:
    return Path(
        goodboy.fetch(filename + ".gz", processor=pooch.Decompress(name=filename))
    )
