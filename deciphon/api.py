from functools import lru_cache
from pathlib import Path

import requests
from blx.cid import CID
from blx.progress import Progress

from deciphon.config import get_config
from deciphon.models import DBCreate, HMMCreate, ScanCreate
from deciphon.storage import storage_has, storage_put

__all__ = ["API", "get_api"]


class API:
    @property
    def root(self):
        cfg = get_config()
        proto = cfg.api_proto
        host = cfg.api_host
        port = cfg.api_port
        prefix = cfg.api_prefix
        return f"{proto}://{host}:{port}{prefix}"

    @property
    def key(self):
        return {"X-API-Key": get_config().api_key}

    def _create_hmm(self, hmm: HMMCreate):
        r = requests.post(self.root + "/hmms/", json=hmm.dict(), headers=self.key)
        r.raise_for_status()

    def create_hmm(self, hmm: Path):
        cid = CID.from_file(hmm, progress=Progress("Hash"))
        if not storage_has(cid):
            storage_put(cid, hmm)

        self._create_hmm(HMMCreate(sha256=cid.hex(), filename=hmm.name))

    def read_hmms(self):
        r = requests.get(self.root + "/hmms")
        r.raise_for_status()
        return r.json()

    def read_hmm(self, hmm_id: int):
        r = requests.get(self.root + f"/hmms/{hmm_id}")
        r.raise_for_status()
        return r.json()

    def _create_db(self, db: DBCreate):
        r = requests.post(self.root + "/dbs/", json=db.dict(), headers=self.key)
        r.raise_for_status()

    def create_db(self, db: Path):
        cid = CID.from_file(db, progress=Progress("Hash"))
        if not storage_has(cid):
            storage_put(cid, db)

        self._create_db(DBCreate(sha256=cid.hex(), filename=db.name))

    def read_dbs(self):
        r = requests.get(self.root + "/dbs")
        r.raise_for_status()
        return r.json()

    def read_db(self, db_id: int):
        r = requests.get(self.root + f"/dbs/{db_id}")
        r.raise_for_status()
        return r.json()

    def create_scan(self, scan: ScanCreate):
        r = requests.post(self.root + "/scans/", json=scan.dict())
        r.raise_for_status()

    def read_scans(self):
        r = requests.get(self.root + "/scans")
        r.raise_for_status()
        return r.json()

    def read_scan(self, scan_id: int):
        r = requests.get(self.root + f"/scans/{scan_id}")
        r.raise_for_status()
        return r.json()

    def read_jobs(self):
        r = requests.get(self.root + "/jobs")
        r.raise_for_status()
        return r.json()

    def read_job(self, job_id: int):
        r = requests.get(self.root + f"/jobs/{job_id}")
        r.raise_for_status()
        return r.json()


@lru_cache
def get_api() -> API:
    return API()
