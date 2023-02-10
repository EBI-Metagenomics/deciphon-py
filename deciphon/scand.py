import asyncio
import json
import os
import shutil
import signal
from pathlib import Path

from blx.cid import CID
from deciphon_core.scan import Scan as ScanCore
from gmqtt import Client as MQTTClient
from h3daemon.hmmfile import HMMFile
from h3daemon.hmmpress import hmmpress
from h3daemon.manager import H3Manager

from deciphon.api import API
from deciphon.config import get_config
from deciphon.models import DB, Scan
from deciphon.storage import storage_get

STOP = asyncio.Event()


def on_connect(client, *_):
    client.subscribe("/deciphon/scan")


def on_message(client, topic, payload, qos, properties):
    del client
    del topic
    del qos
    del properties
    print("On MESSAGE")
    scan = Scan.parse_obj(API().read_scan(int(payload)))
    db = DB.parse_obj(API().read_db(scan.db_id))

    scan_seqs = scan.dict()["seqs"]
    for i in scan_seqs:
        i["scan_id"] = scan.id

    seqs_tmp = Path("seqs_tmp.json")
    with open(seqs_tmp, "w", encoding="utf-8") as fp:
        json.dump(scan_seqs, fp, ensure_ascii=True)

    force = True

    storage_get(CID(db.sha256), Path(db.filename))
    dbfile = Path(db.filename)

    hmmfile = Path(dbfile.stem + ".hmm")
    hmmfiled = HMMFile(hmmfile)
    with H3Manager() as h3:
        hmmpress(hmmfiled)
        pod = h3.start_daemon(hmmfiled, force=True)
        with ScanCore(hmmfile, seqs_tmp, pod.host_port) as x:
            if force:
                if Path(x.product_name).exists():
                    os.unlink(x.product_name)

                if Path(x.base_name).exists():
                    shutil.rmtree(x.base_name)
            x.run()

    # db = Path(Path(hmm.filename).stem + ".dcp")


def on_disconnect(*_):
    print("Disconnected")


def on_subscribe(*_):
    print("SUBSCRIBED")


def ask_exit(*_):
    STOP.set()


async def scand():
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    client = MQTTClient(None)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    cfg = get_config()
    await client.connect(cfg.mqtt_host, cfg.mqtt_port)
    try:
        await STOP.wait()
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(scand())
