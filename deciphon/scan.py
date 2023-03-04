from deciphon_core.scan import Scan as ScanCore

from deciphon.hmmfile import HMMFile
from deciphon.prodfile import ProdFile
from deciphon.seqfile import SeqFile

__all__ = ["Scan"]


class Scan(ScanCore):
    def __init__(self, hmm: HMMFile, seq: SeqFile, prod: ProdFile):
        super().__init__(hmm.path, hmm.dbfile, seq, prod.basedir)
