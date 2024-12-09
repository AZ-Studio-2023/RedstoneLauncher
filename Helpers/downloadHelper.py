import aria2p
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
import requests
from Helpers.getValue import RPC_PORT, getDownloadData
import json
import os
import concurrent.futures
import time


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



class Downloader:
    def __init__(self, tasks: list) -> None:
        """
        Downloader / 下载器用于多线程下载文件。

        :param tasks: tasks是一个包含元组的列表，每个元组为(url, target_path)
        """
        self.tasks = tasks

    def download_file(self, url: str, path: str):
        aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=RPC_PORT,
            secret=""
        )
        )
        event = aria2.add_uris([url], options={"dir": path})
        return event

    def download_files_with_threads(self, max_workers=None):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.download_file, url, target_path): (url, target_path) for url, target_path in self.tasks
            }

            for future in concurrent.futures.as_completed(futures):
                url, target_path = futures[future]
                try:
                    future.result()  # 获取结果，如果下载过程中有异常，这里会重新抛出
                except Exception as exc:
                    logger.error(f'Thread for {url} generated an exception: {exc}')


# 使用示例：
# file_urls_and_paths = [('http://example.com/file1.zip', 'file1.zip'), ('http://example.com/file2.zip', 'file2.zip')]
# downloader = Downloader(file_urls_and_paths)
# downloader.download_files_with_threads(5)  # 同时最多开启5个线程下载




def download_mc(version, aria2c_path, fold=".minecraft"):



    os.system(f"{aria2c_path} -o {fold}/versions/{version}/{version}.jar https://bmclapi2.bangbang93.com/version/{version}/client")
    os.system(f"{aria2c_path} -o {fold}/versions/{version}/{version[0: -2]}.json https://bmclapi2.bangbang93.com/version/{version}/json")



    with open(f"{fold}/versions/{version}/{version[0: -2]}.json", "r") as file:
        libraries_json = file.read()
        libraries_json = json.loads(libraries_json)
        libraries = libraries_json["libraries"]

        libraries_downloads = []

        for i in libraries:
            libraries_downloads.append([i["downloads"]["artifact"]["url"], f"{fold}/versions/{version}/libraries/" + i["downloads"]["artifact"]["path"]])




    try:
        os.makedirs(f"{fold}/assets/indexes/")

    except:
        pass

    with open(f"{fold}/assets/indexes/{version}.json", "w") as f:
        response = requests.get(libraries_json["assetIndex"]["url"])
        response.encoding = "utf-8"
        f.write(response.text)

        json_assets = json.loads(response.text)["objects"]


        assets_downloads = libraries_downloads

        for i in json_assets:
            assets_downloads.append([f"https://resources.download.minecraft.net/{json_assets[i]['hash'][0: 2]}/{json_assets[i]['hash']}", f"{fold}/assets/objects/{json_assets[i]['hash'][0: 2]}/{json_assets[i]['hash']}"])
        downloader = Downloader(assets_downloads)
        downloader.download_files_with_threads(8)

        return

def download_forge_mc(mc_version, aria2c_path, forge_ver, mirror_url, fold=".,minecraft"):
    download_mc(mc_version, aria2c_path, fold)
    response = requests.get(f"https://maven.minecraftforge.net/net/minecraftforge/forge/{mc_version}-{forge_ver}/forge-{mc_version}-{forge_ver}-installer.jar")
    with open("tmp.jar", "wb") as f:
        f.write(response.content)
    os.system(f"java -jar tmp.jar nogui --mirror {mirror_url} --installClient")

def download_fabric_mc(mc_version, aria2c_path, fabric_ver, mirror_url_ma, mirror_url_me, fold=".,minecraft"):
    download_mc(mc_version, aria2c_path, fold)
    response = requests.get(f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{fabric_ver}/fabric-installer-{fabric_ver}.jar")
    with open("tmp.jar", "wb") as f:
        f.write(response.content)
    os.system(f"java -jar tmp.jar client -dir {fold} --mcversion {mc_version} -loader {fabric_ver} -mavenurl {mirror_url_ma} -metaurl {mirror_url_me}")

a = time.time()
download_mc("1.19.2", "./aria2c")
b = time.time()
print(b - a)







