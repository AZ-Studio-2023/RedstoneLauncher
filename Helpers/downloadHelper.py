import os
import subprocess
import time
from urllib.parse import urlsplit

import aria2p
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool
import requests

from Helpers.Config import cfg
from Helpers.getValue import RPC_PORT, getDownloadData, CACHE_PATH, setDownloadData, getVersionsData, setVersionsData
import json

from Helpers.outputHelper import logger

aria2 = aria2p.API(aria2p.Client(
    host="http://localhost",
    port=RPC_PORT,
    secret=""
))

def get_first_stable_ver(lst):
    for item in lst:
        if item.get('stable'):
            return item
    return None

def get_filename_from_url(url):
    path = urlsplit(url).path
    filename = os.path.basename(path)
    return filename

def get_download_status():
    global aria2
    # 获取当前所有的下载任务
    downloads = aria2.get_downloads()
    downloads = [task for task in downloads if task.status == 'active']
    # 如果没有下载任务，返回提示信息
    if not downloads:
        if not getVersionsData()["installing"]:
            return "没有正在进行的下载任务。"
        else:
            return "正在安装模组加载器"

    # 总的已下载大小和总大小
    total_downloaded = 0
    total_size = 0
    total_speed = 0  # 初始化总速度

    # 计算总进度和总速度
    for download in downloads:
        downloaded = download.completed_length  # 已下载的字节数
        size = download.total_length  # 任务总大小（字节数）
        speed = download.download_speed  # 任务下载速度（字节/秒）

        # 更新总已下载大小、总大小和总速度
        total_downloaded += downloaded
        total_size += size
        total_speed += speed  # 累加下载速度

    # 计算总进度
    if total_size > 0:
        total_progress = (total_downloaded / total_size) * 100
    else:
        total_progress = 0

    # 生成总进度条
    total_progress_bar = "#" * int((total_progress / 100) * 40)  # 使用 40 个字符表示总进度
    total_progress_bar = total_progress_bar.ljust(40)  # 确保进度条的长度为 40
    total_speed_human = convert_bytes(total_speed)  # 格式化总速度
    total_progress_line = f"总进度: {total_progress:.2f}% | {total_progress_bar} | {total_downloaded}/{total_size} bytes | 速度: {total_speed_human}/s\n"

    # 创建一个结果字符串，先加入总进度
    status_string = total_progress_line + "\n"

    # 获取并显示每个任务的进度
    for download in downloads:
        # 计算任务的进度
        progress = download.progress / 100  # 进度百分比转为小数
        progress_bar = "#" * int(progress * 40)  # 使用 40 个字符表示进度条
        progress_bar = progress_bar.ljust(40)  # 确保进度条的长度为 40
        progress_percentage = f"{download.progress:.2f}%"

        # 每个任务的进度信息，文件名放在最左侧
        task_status = f"{download.name} | {progress_percentage} | {progress_bar} | {download.completed_length}/{download.total_length} bytes\n"

        # 拼接到结果字符串
        status_string += task_status

    return status_string


def convert_bytes(byte_size):
    """将字节数转换为合适的单位（B, KB, MB, GB）"""
    if byte_size < 1024:
        return f"{byte_size} B"
    elif byte_size < 1024 ** 2:
        return f"{byte_size / 1024:.2f} KB"
    elif byte_size < 1024 ** 3:
        return f"{byte_size / 1024 ** 2:.2f} MB"
    else:
        return f"{byte_size / 1024 ** 3:.2f} GB"

def mirrorURL(url: str):
    if cfg.source.value != "官方":
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
        elif "https://meta.fabricmc.net/" in url:
            url = url.replace("https://meta.fabricmc.net/", "https://bmclapi2.bangbang93.com/fabric-meta/")
        elif "https://maven.fabricmc.net/" in url:
            url = url.replace("https://maven.fabricmc.net/", "https://bmclapi2.bangbang93.com/maven/")
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
    global aria2
    if os.path.exists(path):
        return
    dir_path = os.path.dirname(path)
    file_name = os.path.basename(path)

    event = aria2.add_uris([url], options={
        "dir": dir_path,
        "out": file_name
    })
    return event

def getFinish():
    global aria2
    downloads = aria2.get_downloads()
    downloads = [task for task in downloads if task.status == 'active']
    if not downloads:
        return True
    else:
        return False


def download_file(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        return True
    else:
        return False

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
        mc_type:str = version_dic["type"]
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

        versionData["type"] = mc_type
        versionData["clientVersion"] = self.version
        f = open(os.path.join(cfg.gamePath.value, "versions", self.name, f'{self.name}.json'), "w")
        f.write(json.dumps(versionData, indent=4))
        f.close()

        # 下载游戏Jar
        url = versionData["downloads"]["client"]["url"]
        url = mirrorURL(url)
        download(url, os.path.join(cfg.gamePath.value, "versions", self.name, f'{self.name}.jar'))

        # 下载依赖库
        for lib in versionData["libraries"]:
            if "artifact" in lib["downloads"] and "classifiers" not in lib["downloads"]:
                url = lib["downloads"]["artifact"]["url"]
                url = mirrorURL(url)
                dir_path = os.path.join(cfg.gamePath.value, "libraries", os.path.dirname(lib["downloads"]["artifact"]["path"]))
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                download(url, os.path.join(cfg.gamePath.value, "libraries", lib["downloads"]["artifact"]["path"]))
            elif "classifiers" in lib["downloads"]:
                url = lib["downloads"]["artifact"]["url"]
                url = mirrorURL(url)
                dir_path = os.path.join(cfg.gamePath.value, "libraries",
                                        os.path.dirname(lib["downloads"]["artifact"]["path"]))
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                download(url, os.path.join(cfg.gamePath.value, "libraries", lib["downloads"]["artifact"]["path"]))

                for cl in lib["downloads"]["classifiers"].values():
                    try:
                        url = cl["url"]
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
                    try:
                        if cfg.source.value == "官方":
                            url = f"https://resources.download.minecraft.net/{obj['hash'][0:2]}/{obj['hash']}"
                        else:
                            url = f"https://bmclapi2.bangbang93.com/assets/{obj['hash'][0:2]}/{obj['hash']}"
                        path = os.path.join(cfg.gamePath.value, "assets", "objects", obj['hash'][0:2])
                        if not os.path.exists(path):
                            os.makedirs(path)
                        download(url, os.path.join(cfg.gamePath.value, "assets", "objects", obj['hash'][0:2], obj['hash']))
                    except Exception as e:
                        logger.error(f"下载资源文件出错：{e}")

        # 模组端
        if self.modsLoader == "fabric":
            r = requests.get(mirrorURL("https://meta.fabricmc.net/v2/versions/installer")).json()
            url = get_first_stable_ver(r)["url"]
            if not url is None:
                d = getVersionsData()
                d["installing"] = True
                setVersionsData(d)
                if not download_file(url, os.path.join(CACHE_PATH, get_filename_from_url(url))):
                    logger.error("下载错误")
                command = f"{cfg.javaPath.value} -jar {os.path.join(CACHE_PATH, get_filename_from_url(url))} client -mcversion {self.version} -loader {self.modsLoaderVersion} -dir {cfg.gamePath.value} "
                if mc_type == "snapshot":
                    command = command + "-snapshot "
                if cfg.source.value != "官方":
                    command = command + "-mavenurl https://bmclapi2.bangbang93.com/maven/ -metaurl https://bmclapi2.bangbang93.com/fabric-meta/"
                command = command + " nogui"
                logger.info(command)
                process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                 creationflags=subprocess.CREATE_NO_WINDOW)
                process.wait()
                d = getVersionsData()
                d["installing"] = False
                setVersionsData(d)






