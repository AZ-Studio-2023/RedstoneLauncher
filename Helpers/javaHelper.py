import os
import re
import concurrent.futures
import subprocess
import sys
from platform import system
from subprocess import Popen, PIPE

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication

from Helpers.getValue import DEFAULT_GAME_PATH
from Helpers.outputHelper import logger


class javaPath:
    def __init__(self, path, version):
        self.path = path
        self.version = version

    def to_dict(self):
        return {"Path": self.path, "Version": self.version}


def get_java_version(file_path):
    try:
        process = Popen([file_path, "-version"], stdout=PIPE, stderr=PIPE)
        _, stderr = process.communicate()
        output = stderr.decode()
        version_pattern = r'(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[._](\d+))?(?:-(.+))?'
        version_match = re.search(version_pattern, output)
        if version_match:
            version = ".".join(filter(None, version_match.groups()))
            return version
    except Exception as e:
        logger.error(f"获取Java版本时出错：{e}")
    return "Unknown"


def find_java_directories(base_path, match_keywords, exclude_keywords):
    java_list = []
    java_path_list = []
    try:
        for root, dirs, files in os.walk(base_path):
            for dir_name in dirs:
                if any(exclude in dir_name for exclude in exclude_keywords):
                    continue
                if any(keyword in dir_name.lower() for keyword in match_keywords):
                    java_path = os.path.normpath(os.path.join(root, dir_name, 'bin',
                                             'java.exe' if "windows" in system().lower() else 'java'))
                    if os.path.isfile(java_path):
                        if not java_path in java_path_list:
                            version = get_java_version(java_path)
                            if version:
                                java_path_list.append(java_path)
                                java_list.append(javaPath(java_path, version))
    except Exception as e:
        print(f"Error searching directory {base_path}: {e}")
    return java_list


class GetJava_Global(QThread):
    finished = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.match_keywords = [
            "bin", "java", "jdk", "jre", "minecraft", "launcher", "pcl", "hmcl"
        ]
        self.exclude_keywords = ["$", "{", "}", "__"]
        self.num_threads = 20
        if system().lower() == "windows":
            self.start_paths = [f"{chr(i)}:\\" for i in range(65, 91) if os.path.exists(f"{chr(i)}:\\")]
        else:
            self.start_paths = ["/usr", "/usr/java", "/usr/lib/jvm", "/usr/lib64/jvm", "/opt/jdk", "/opt/jdks"]

    def run(self):
        java_list = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            future_to_path = {
                executor.submit(find_java_directories, path, self.match_keywords, self.exclude_keywords): path for path
                in self.start_paths}
            for future in concurrent.futures.as_completed(future_to_path):
                java_list.extend(future.result())
        self.finished.emit(java_list)

class GetJava_Local(QThread):
    finished = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.match_keywords = [
            "bin", "java", "jdk", "jre", "minecraft", "launcher", "pcl", "hmcl"
        ]
        self.exclude_keywords = ["$", "{", "}", "__"]
        self.num_threads = 20
        if system().lower() == "windows":
            self.start_paths = [DEFAULT_GAME_PATH]

        else:
            self.start_paths = ["/usr", "/usr/java", "/usr/lib/jvm", "/usr/lib64/jvm", "/opt/jdk", "/opt/jdks"]

    def run(self):
        java_list = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            future_to_path = {
                executor.submit(find_java_directories, path, self.match_keywords, self.exclude_keywords): path for
                path
                in self.start_paths}
            for future in concurrent.futures.as_completed(future_to_path):
                java_list.extend(future.result())
            path_list = os.environ.get('PATH').split(';')
            for env_path in path_list:
                if os.path.exists(os.path.join(env_path, "java.exe")) and os.path.isfile(os.path.join(env_path, "java.exe")):
                    add_paths = []
                    for obj in java_list:
                        add_paths.append(obj.path)
                    if not os.path.normpath(os.path.join(env_path, "java.exe")) in add_paths:
                        java_list.append(javaPath(os.path.normpath(os.path.join(env_path, "java.exe")), get_java_version(os.path.join(env_path, "java.exe"))))
        self.finished.emit(java_list)