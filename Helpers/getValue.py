import os
from datetime import date

from PyQt5.QtCore import QStandardPaths

VERSION = "0.0.18 Preview"
UPDATE_NUMBER = 1
versionDetail = "1.还没写！"
YEAR = int(date.today().year)
AUTHOR = "AZ Studio"
FEEDBACK_URL = "https://github.com/AZ-Studio-2023/RedstoneLauncher/issues"
RELEASE_URL = "https://github.com/AZ-Studio-2023/RedstoneLauncher/releases/"
AZ_URL = "https://azteam.cn"
HELP_URL = "https://azteam.cn"
CLIENT_ID = "846a8cc1-cc50-4df5-a2df-ea391aac13c5"
REDIRECT_URL = "http://localhost:60000"


MINECRAFT_ICON = "resource/image/core/minecraft.png"
FORGE_ICON = "resource/image/core/forge.png"
FABRIC_ICON = "resource/image/core/fabric.png"
MICROSOFT_ACCOUNT = "resource/image/account/Microsoft.png"
LEGACY_ACCOUNT = "resource/image/account/legacy.png"
THIRD_PARTY_ACCOUNT = "resource/image/account/third_party.png"
JAVA_RUNTIME = "resource/image/java.png"
SNAPSHOT = "resource/image/block/obsidian.png"
RELEASE = "resource/image/block/grass_block.png"

ARIA2C_PATH = 'resource/aria2/aria2c.exe'
RPC_PORT = 6800
DEFAULT_GAME_PATH = os.path.join(os.path.expanduser('~'), "AppData", "Roaming", ".minecraft")
PLU_URL = ""

config_path_value = str(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
allPath = os.path.join(config_path_value, "RedstoneLauncher")
DATA_PATH = os.path.join(allPath, "data")
ACCOUNTS_PATH = os.path.join(DATA_PATH, "accounts.json")
COMMAND_PATH = os.path.join(allPath, "command")
CONFIG_PATH = os.path.join(DATA_PATH, "config.json")
CACHE_PATH = os.path.join(allPath, "cache")
LOG_PATH = os.path.join(allPath, "log")

LAUNCH_DATA = {}

PROCESS_DATA = []

DOWNLOAD_DATA = []

def setLaunchData(data):
    global LAUNCH_DATA
    LAUNCH_DATA = data

def getLaunchData():
    global LAUNCH_DATA
    return LAUNCH_DATA
def setProcessData(data):
    global PROCESS_DATA
    PROCESS_DATA = data

def getProcessData():
    global PROCESS_DATA
    return PROCESS_DATA

def setDownloadData(data):
    global DOWNLOAD_DATA
    DOWNLOAD_DATA = data

def getDownloadData():
    global DOWNLOAD_DATA
    return DOWNLOAD_DATA




