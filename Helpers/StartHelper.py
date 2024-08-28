import os
import json
import subprocess
import zipfile
import platform

from Helpers.Config import cfg
from Helpers.flyoutmsg import dlerr
from Helpers.getValue import getLaunchData
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QRunnable

from Helpers.outputHelper import logger
from Helpers.pluginHelper import plugins_api_items

plugins_api = plugins_api_items


class WorkerSignals(QObject):
    progress = pyqtSignal(dict)


def decompression(filename: str, path: str):
    try:
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(path)
        return 0
    except FileNotFoundError:
        return "Error"


def getVersionType(gameDir, version):
    with open(os.path.join(gameDir, 'versions', version, f'{version}.json'), "r") as u:
        file_content = u.read()
        if "forge" in file_content:
            return "Forge"
        elif "fabric" in file_content:
            return "Fabric"
        else:
            return "Vanilla"


def getAllVersion(gameDir):
    versions = os.listdir(os.path.join(gameDir, 'versions'))
    versions = [version for version in versions if os.path.isdir(os.path.join(gameDir, 'versions', version))]
    version_list = []
    for v in versions:
        with open(os.path.join(gameDir, 'versions', v, f'{v}.json'), "r") as u:
            file_content = u.read()
            if "forge" in file_content:
                version_list.append({"name": v, "type": "Forge"})
            elif "fabric" in file_content:
                version_list.append({"name": v, "type": "Fabric"})
            else:
                version_list.append({"name": v, "type": "Vanilla"})
    return version_list


def getVersionInfo(gameDir, version):
    with open(os.path.join(gameDir, 'versions', version, f'{version}.json'), "r") as u:
        file_content = json.loads(u.read())
        return {"type": file_content["clientVersion"], "clientVersion": file_content["clientVersion"]}


class launch(QRunnable):
    def __init__(self):
        super(launch, self).__init__()
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        global plugins_api
        for item in plugins_api:
            try:
                plugins_api[item].when_beginning()
            except Exception as e:
                if cfg.debug_card.value:
                    logger.error(f"插件{item}出现错误：{e}")

        data = getLaunchData()
        main_class = "net.minecraft.client.main.Main"
        pc_os = platform.system()
        assetsDir = os.path.join(data["gameDir"], "assets")
        if len(data["clientVersion"]) >= 3 and data["clientVersion"][2] == '.':
            assetIndex = data["clientVersion"][:3]
        else:
            assetIndex = data["clientVersion"][:4]
        native_library = str(os.path.join(data["gameDir"], "versions", data["version"], f"{data['version']}-natives"))
        self.signals.progress.emit({"state": "0", "uuid": data["process_uuid"]})
        logger.debug(f"Version: {data['version']} | Process_UUID: {data['process_uuid']} | 当前状态：补全游戏所需资源")

        native_list = []
        native_list.append(os.path.join(data["gameDir"], "versions", data["version"], f"{data['version']}.jar"))
        version_path = os.path.join(data["gameDir"], "versions", data["version"], f"{data['version']}.json")
        version_json = open(version_path, "r")
        version_data = json.loads(version_json.read())
        for libraries in version_data["libraries"]:
            try:
                for native in libraries["downloads"]:
                    if native == "artifact":
                        dirct_path = native_library
                        file_path = str(
                            os.path.normpath(
                                os.path.join(data["gameDir"], "libraries", libraries["downloads"][native]['path'])))
                        if not os.path.exists(f"command/{data['version']}.bat"):
                            if decompression(file_path, dirct_path) == 0:
                                native_list.append(file_path)
                        else:
                            native_list.append(file_path)
                    elif native == 'classifiers':
                        for n in libraries['downloads'][native].values():
                            dirct_path = str(
                                os.path.join(data["gameDir"], "libraries", libraries["downloads"][native]['path']))
                            file_path = str(os.path.join(data["gameDir"], "libraries", n["path"]))
                            if not os.path.exists(f"{data['version']}.bat"):
                                decompression(file_path, dirct_path)
            except KeyError:
                continue
        if data["gameType"] != "Vanilla":
            for mod in os.listdir(os.path.join(data["gameDir"], 'mods')):
                if mod.lower().endswith('.jar'):
                    native_list.append(os.path.join(data["gameDir"], 'mods', mod))
        self.signals.progress.emit({"state": "1", "uuid": data["process_uuid"]})
        logger.debug(f"Version: {data['version']} | Process_UUID: {data['process_uuid']} | 当前状态：构建启动命令")
        # 构建本地库字符串
        if pc_os == "Windows":
            cp = ';'.join(native_list)
        else:
            cp = ':'.join(native_list)
        # 构建启动命令
        jvm_args = [
            f"-Xmx{data['xmx']}m",
            "-XX:+UseG1GC",
            "-XX:-UseAdaptiveSizePolicy",
            "-XX:-OmitStackTraceInFastThrow",
            f"-Djava.library.path={native_library}",
            f"-Dminecraft.launcher.brand=Redstone Launcher",
            f"-Dminecraft.launcher.version=0.9.6",
            f"-Dos.name={pc_os} {platform.version()}",
            f"-Dos.version={platform.version()}",
            "-cp",
            f"{cp}"
        ]

        mc_args = [
            main_class,
            "--username", data["username"],
            "--version", data['clientVersion'],
            "--gameDir", data["gameDir"],
            "--assetsDir", assetsDir,
            "--assetIndex", assetIndex,
            "--uuid", data["uuid"],
            "--accessToken", data["accessToken"],
            "--userType", data["userType"],
            "--versionType", data["versionType"]
        ]
        command = [data["javaDir"]] + jvm_args + mc_args
        u = open(f"command/{data['version']}.bat", "w")
        command_bat = subprocess.list2cmdline(command)
        u.write(str(command_bat))
        u.close()
        game_log_path = os.path.join("log", data["process_uuid"])
        if not os.path.exists(game_log_path):
            os.mkdir(game_log_path)
        self.signals.progress.emit({"state": "2", "uuid": data["process_uuid"]})
        logger.debug(f"Version: {data['version']} | Process_UUID: {data['process_uuid']} | 当前状态：游戏进程已启动")
        for item in plugins_api:
            try:
                plugins_api[item].when_startup()
            except Exception as e:
                if cfg.debug_card.value:
                    logger.error(f"插件{item}出现错误：{e}")
        result = subprocess.run(command, capture_output=True, text=True, cwd=game_log_path)
        self.signals.progress.emit({"state": "3", "uuid": data["process_uuid"]})
        logger.debug(f"Version: {data['version']} | Process_UUID: {data['process_uuid']} | 当前状态：游戏进程已退出")
        for item in plugins_api:
            try:
                plugins_api[item].when_stopping()
            except Exception as e:
                if cfg.debug_card.value:
                    logger.error(f"插件{item}出现错误：{e}")
