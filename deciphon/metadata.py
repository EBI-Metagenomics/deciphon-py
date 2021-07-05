from dataclasses import dataclass

__all__ = ["Metadata"]


@dataclass
class Metadata:
    name: str
    acc: str
