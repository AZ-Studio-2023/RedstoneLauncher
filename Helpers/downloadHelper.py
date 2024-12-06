import aria2p
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
import requests
from Helpers.getValue import RPC_PORT, getDownloadData
import json

from Helpers.outputHelper import logger


class WorkerSignals(QObject):
    progress = pyqtSignal(str)

class downloadJson(QRunnable):
    def __init__(self):
        super(downloadJson, self).__init__()
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        d = getDownloadData()
        url = d["url"]
        path = d["path"]
        try:
            data = requests.get(url).json()
        except Exception as e:
            logger.error(e)
            self.signals.progress.emit("error")
            return
        f = open(path, "w")
        f.write(json.dumps(data))
        f.close()
        self.signals.progress.emit("ok")

    def flush(self):
        pass

def download(url, path):
    aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=RPC_PORT,
            secret=""
        )
    )
    event = aria2.add_uris([url], options={"dir": path})
    return event
