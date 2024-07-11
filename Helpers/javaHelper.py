import os
import subprocess
from platform import system
from PyQt5.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, Qt

# 关键词列表
keywords = [
    'java', 'jdk', 'jre'
]


class JavaDetector(QRunnable):
    """
    A worker class to find Java installations in candidate directories.
    """
    java_found = pyqtSignal(dict)

    def __init__(self, dir_path):
        super().__init__()
        self.dir_path = dir_path

    def run(self):
        java_list = self.find_javaw(self.dir_path)
        for java in java_list:
            self.java_found.emit(java)

    def get_java_version(self, java_path):
        try:
            result = subprocess.run([java_path, '-version'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            output = result.stderr
            version_line = output.split('\n')[0]
            version = version_line.split('"')[1]
            return version
        except Exception as e:
            print(f"Error getting version for {java_path}: {e}")
            return "Unknown"

    def find_javaw(self, candidate_dirs):
        java_list = []
        for dir_path in candidate_dirs:
            for root, _, files in os.walk(dir_path):
                if "javaw.exe" in files:
                    java_path = os.path.join(root, "javaw.exe")
                    version = self.get_java_version(java_path)
                    java_list.append({"name": f"JDK {version}", "path": java_path})
        return java_list


def search_keywords(start_path, keywords):
    """
    搜索包含关键词的目录。
    """
    candidate_dirs = []
    for root, dirs, _ in os.walk(start_path):
        for dir_name in dirs:
            for keyword in keywords:
                if keyword.lower() in dir_name.lower():
                    candidate_dirs.append(os.path.join(root, dir_name))
                    break
    return candidate_dirs


def detect_all_javaw():
    """
    检测所有已安装的javaw.exe路径，并返回包含路径和版本信息的字典列表。
    """
    java_list = []
    candidate_dirs = []

    if system().lower() == 'windows':
        for drive in range(ord('C'), ord('Z') + 1):
            drive_path = f"{chr(drive)}:\\"
            if os.path.exists(drive_path):
                candidate_dirs.extend(search_keywords(drive_path, keywords))
    else:
        # 假定在类Unix系统上
        default_paths = ["/usr", "/usr/lib", "/usr/local", "/opt"]
        for path in default_paths:
            if os.path.exists(path):
                candidate_dirs.extend(search_keywords(path, keywords))

    # 使用QThreadPool多线程并行查找javaw.exe
    threadpool = QThreadPool.globalInstance()
    threadpool.setMaxThreadCount(16)  # 设置最大线程数为16（根据需要调整）

    for dir_path in candidate_dirs:
        worker = JavaDetector(dir_path)
        worker.java_found.connect(lambda java: java_list.append(java))
        threadpool.start(worker)

    # 等待所有线程完成
    threadpool.waitForDone()

    return java_list


# 调用检测函数并打印结果
java_installations = detect_all_javaw()
for java in java_installations:
    print(java)
