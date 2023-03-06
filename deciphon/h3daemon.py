from h3daemon.hmmfile import HMMFile as H3File
from h3daemon.sched import SchedContext

from deciphon.hmmfile import HMMFile

__all__ = ["H3Daemon"]


class H3Daemon:
    def __init__(self, hmmfile: HMMFile) -> None:
        self._hmmfile = hmmfile
        self._sched_ctx = SchedContext(H3File(hmmfile.path))
        self._port: int = -1

    @property
    def port(self):
        return self._port

    def __enter__(self):
        sched = self._sched_ctx.__enter__()
        sched.is_ready(wait=True)
        self._port = sched.master.get_port()
        return self

    def __exit__(self, *_):
        self._sched_ctx.__exit__(*_)
