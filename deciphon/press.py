from deciphon_core.press import Press as CorePress

from deciphon.hmmfile import HMMFile

__init__ = ["Press"]


class Press(CorePress):
    def __init__(self, hmm: HMMFile):
        super().__init__(hmm.path, hmm.dbfile)
