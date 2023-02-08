import os
import shutil
from pathlib import Path
from deciphon_core.scan import Scan
from h3daemon.manager import H3Manager
from h3daemon.hmmfile import HMMFile
from h3daemon.hmmpress import hmmpress

__all__ = ["scan"]


def scan(hmm: Path, seq: Path, force=False):
    hmmfile = HMMFile(hmm)
    with H3Manager() as h3:
        hmmpress(hmmfile)
        pod = h3.start_daemon(hmmfile, force=True)
        with Scan(hmm, seq, pod.host_port) as x:
            if force:
                if Path(x.product_name).exists():
                    os.unlink(x.product_name)

                if Path(x.base_name).exists():
                    shutil.rmtree(x.base_name)
            x.run()
