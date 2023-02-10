import asyncio
import signal
from pathlib import Path

from blx.cid import CID
from blx.progress import Progress
from deciphon_core.press import Press
from gmqtt import Client as MQTTClient

from deciphon.api import API
from deciphon.config import get_config
from deciphon.models import HMM
from deciphon.storage import storage_get, storage_put

STOP = asyncio.Event()


def on_connect(client, *_):
    client.subscribe("/deciphon/hmm")


def on_message(client, topic, payload, qos, properties):
    del client
    del topic
    del qos
    del properties
    print("On MESSAGE")
    hmm = HMM.parse_obj(API().read_hmm(int(payload)))
    print(hmm)
    storage_get(CID(hmm.sha256), Path(hmm.filename))

    db = Path(Path(hmm.filename).stem + ".dcp")
    with Press(hmm.filename, db) as press:
        for _ in press:
            pass

    print("Finished pressing")
    cid = CID.from_file(db, Progress(desc="tmp"))
    storage_put(cid, db)
    API().create_db(db)


def on_disconnect(*_):
    print("Disconnected")


def on_subscribe(*_):
    print("SUBSCRIBED")


def ask_exit(*_):
    STOP.set()


async def pressd():
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
    asyncio.run(pressd())
