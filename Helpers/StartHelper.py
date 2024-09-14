import os
import json
import subprocess
import zipfile
import platform
from PyQt5.QtCore import QThreadPool, pyqtSignal, pyqtSlot, QObject, QRunnable

from Helpers.Config import cfg
from Helpers.MicAuth import refresh_token
from Helpers.flyoutmsg import dlerr
from Helpers.getValue import getLaunchData, ACCOUNTS_PATH, COMMAND_PATH, LOG_PATH
from Helpers.outputHelper import logger
from Helpers.pluginHelper import plugins_api_items

plugins_api = plugins_api_items

def find_dict(dictionary_list, key, value):
    for dictionary in dictionary_list:
        if key in dictionary and dictionary[key] == value:
            return dictionary
    return None

class WorkerSignals(QObject):
    progress = pyqtSignal(dict)


class DecompressionTask(QRunnable):
    def __init__(self, filename, path):
        super(DecompressionTask, self).__init__()
        self.filename = filename
        self.path = path

    @pyqtSlot()
    def run(self):
        try:
            with zipfile.ZipFile(self.filename, 'r') as zip_ref:
                zip_ref.extractall(self.path)
        except FileNotFoundError:
            logger.error(f"未找到文件: {self.filename}")


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
        self.thread_pool = QThreadPool()

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

        if data["userType"] == "msa":
            self.signals.progress.emit({"state": "4", "uuid": data["process_uuid"]})
            logger.debug(f"Version: {data['version']} | Process_UUID: {data['process_uuid']} | 当前状态：刷新登录令牌")
            c_data = refresh_token(data["refresh_token"])
            if c_data["code"] != 200:
                self.signals.progress.emit({"state": "5", "uuid": data["process_uuid"]})
                logger.error("刷新令牌失败！将使用旧的令牌启动")
            else:
                f = open(ACCOUNTS_PATH, "r")
                l_data = json.loads(f.read())["accounts"]
                f.close()
                d = find_dict(l_data, "uuid", c_data["uuid"])
                l_data.remove(d)
                l_data.append({"name": c_data["username"], "type": "msa", "uuid": c_data["uuid"], "refresh_token": c_data["refresh_token"], "access_token": c_data["access_token"]})
                f = open(ACCOUNTS_PATH, "w")
                f.write(json.dumps({"accounts": l_data}))
                f.close()
                data["access_token"] = c_data["access_token"]
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
                        if not os.path.exists(os.path.join(COMMAND_PATH, f"{data['version']}.bat")):
                            task = DecompressionTask(file_path, dirct_path)
                            self.thread_pool.start(task)
                            native_list.append(file_path)
                        else:
                            native_list.append(file_path)
                    elif native == 'classifiers':
                        for n in libraries['downloads'][native].values():
                            dirct_path = str(
                                os.path.join(data["gameDir"], "libraries", libraries["downloads"][native]['path']))
                            file_path = str(os.path.join(data["gameDir"], "libraries", n["path"]))
                            if not os.path.exists(f"{data['version']}.bat"):
                                task = DecompressionTask(file_path, dirct_path)
                                self.thread_pool.start(task)
            except KeyError:
                continue

        if data["gameType"] != "Vanilla":
            for mod in os.listdir(os.path.join(data["gameDir"], 'mods')):
                if mod.lower().endswith('.jar'):
                    native_list.append(os.path.join(data["gameDir"], 'mods', mod))

        self.thread_pool.waitForDone()

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
            "--accessToken", data["access_token"],
            "--userType", data["userType"],
            "--versionType", data["versionType"]
        ]
        command = [data["javaDir"]] + jvm_args + mc_args
        u = open(os.path.join(COMMAND_PATH, f"{data['version']}.bat"), "w")
        command_bat = subprocess.list2cmdline(command)
        u.write(str(command_bat))
        u.close()
        game_log_path = os.path.join(LOG_PATH, data["process_uuid"])
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