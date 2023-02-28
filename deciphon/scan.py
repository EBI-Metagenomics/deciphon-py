import shutil
from pathlib import Path

from deciphon_core.scan import Scan
from h3daemon.hmmfile import HMMFile
from h3daemon.sched import SchedContext

__all__ = ["scan"]


def scan(hmm: HMMFile, seq: Path, force=False):
    hmm.ensure_pressed()
    with SchedContext(hmm) as sched:
        sched.is_ready(True)
        port = sched.master.get_port()
        with Scan(hmm.path, seq, port) as x:
            if force:
                Path(x.product_name).unlink(True)
                if Path(x.base_name).exists():
                    shutil.rmtree(x.base_name)
            x.run()
