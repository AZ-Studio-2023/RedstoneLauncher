import os

import aria2p
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool
import requests

from Helpers.Config import cfg
from Helpers.getValue import RPC_PORT, getDownloadData, CACHE_PATH, setDownloadData
import json

from Helpers.outputHelper import logger

def mirrorURL(url: str):
    if "https://launchermeta.mojang.com/" in url:
        url = url.replace("https://launchermeta.mojang.com/", "https://bmclapi2.bangbang93.com")
    elif "https://launcher.mojang.com/" in url:
        url = url.replace("https://launcher.mojang.com/", "https://bmclapi2.bangbang93.com")
    elif "https://piston-meta.mojang.com" in url:
        url = url.replace("https://piston-meta.mojang.com", "https://bmclapi2.bangbang93.com")
    elif "https://piston-data.mojang.com" in url:
        url = url.replace("https://piston-data.mojang.com", "https://bmclapi2.bangbang93.com")
    elif "https://libraries.minecraft.net/" in url:
        url = url.replace("https://libraries.minecraft.net/", "https://bmclapi2.bangbang93.com/maven/")
    return url


def find_dict(dictionary_list, key, value):
    for dictionary in dictionary_list:
        if key in dictionary and dictionary[key] == value:
            return dictionary
    return None

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
    if os.path.exists(path):
        return
    dir_path = os.path.dirname(path)
    file_name = os.path.basename(path)

    aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=RPC_PORT,
            secret=""
        )
    )
    event = aria2.add_uris([url], options={
        "dir": dir_path,
        "out": file_name
    })
    return event

class downloadSignals(QObject):
    progress = pyqtSignal(str)

class downloadVersions(QRunnable):
    def __init__(self, name, version, modsLoader=None, modsLoaderVersion=None):
        super(downloadVersions, self).__init__()
        self.signals = downloadSignals()
        self.name = name
        self.version = version
        self.modsLoader = modsLoader
        self.modsLoaderVersion = modsLoaderVersion

    @pyqtSlot()
    def run(self):
        # 下载版本JSON
        f = open(os.path.join(CACHE_PATH, "version_manifest.json"), "r")
        data = json.loads(f.read())
        f.close()
        version_dic = find_dict(data["versions"], "id", self.version)
        self.pool = QThreadPool()
        url: str = version_dic["url"]
        if cfg.source.value != "官方":
            url = mirrorURL(url)
        if not os.path.exists(os.path.join(cfg.gamePath.value, "versions", self.name)):
            os.makedirs(os.path.join(cfg.gamePath.value, "versions", self.name))
        setDownloadData({"url": url, "path": os.path.join(cfg.gamePath.value, "versions", self.name, f'{self.name}.json')})
        self.runnable = downloadJson()
        self.pool.start(self.runnable)
        self.pool.waitForDone()

        f = open(os.path.join(cfg.gamePath.value, "versions", self.name, f'{self.name}.json'), "r")
        versionData = json.loads(f.read())
        f.close()

        # 下载游戏Jar
        url = versionData["downloads"]["client"]["url"]
        if cfg.source.value != "官方":
            url = mirrorURL(url)
        download(url, os.path.join(cfg.gamePath.value, "versions", self.name, f'{self.name}.jar'))

        # 下载依赖库
        for lib in versionData["libraries"]:
            if "artifact" in lib["downloads"] and "classifiers" not in lib["downloads"]:
                url = lib["downloads"]["artifact"]["url"]
                if cfg.source.value != "官方":
                    url = mirrorURL(url)
                dir_path = os.path.join(cfg.gamePath.value, "libraries", os.path.dirname(lib["downloads"]["artifact"]["path"]))
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                download(url, os.path.join(cfg.gamePath.value, "libraries", lib["downloads"]["artifact"]["path"]))
            elif "classifiers" in lib["downloads"]:
                url = lib["downloads"]["artifact"]["url"]
                if cfg.source.value != "官方":
                    url = mirrorURL(url)
                dir_path = os.path.join(cfg.gamePath.value, "libraries",
                                        os.path.dirname(lib["downloads"]["artifact"]["path"]))
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                download(url, os.path.join(cfg.gamePath.value, "libraries", lib["downloads"]["artifact"]["path"]))

                for cl in lib["downloads"]["classifiers"].values():
                    try:
                        url = cl["url"]
                        if cfg.source.value != "官方":
                            url = mirrorURL(url)
                        dir_path = os.path.join(cfg.gamePath.value, "libraries",
                                                os.path.dirname(cl["path"]))
                        if not os.path.exists(dir_path):
                            os.makedirs(dir_path)
                        download(url, os.path.join(cfg.gamePath.value, "libraries", cl["path"]))
                    except Exception as e:
                        logger.error(f"错误：{e}")
                        continue


                # 下载资源索引
                url = versionData["assetIndex"]["url"]
                if cfg.source.value != "官方":
                    url = mirrorURL(url)
                assets_path = os.path.join(cfg.gamePath.value, "assets", "indexes")
                if not os.path.exists(assets_path):
                    os.makedirs(assets_path)
                setDownloadData(
                    {"url": url, "path": os.path.join(assets_path, f"{versionData['assetIndex']['id']}.json")})
                self.runnable = downloadJson()
                self.pool.start(self.runnable)
                self.pool.waitForDone()

                # 下载资源文件
                f = open(os.path.join(assets_path, f"{versionData['assetIndex']['id']}.json"), "r")
                assetsData = json.loads(f.read())
                f.close()
                for obj in assetsData["objects"].values():
                    if cfg.source.value == "官方":
                        url = f"https://resources.download.minecraft.net/{obj['hash'][0:2]}/{obj['hash']}"
                    else:
                        url = f"https://bmclapi2.bangbang93.com/assets/{obj['hash'][0:2]}/{obj['hash']}"
                    path = os.path.join(cfg.gamePath.value, "assets", "objects", obj['hash'][0:2])
                    if not os.path.exists(path):
                        os.makedirs(path)
                    download(url, os.path.join(cfg.gamePath.value, "assets", "objects", obj['hash'][0:2], obj['hash']))



