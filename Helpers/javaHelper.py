import os
import re
import concurrent.futures
from platform import system
from subprocess import Popen, PIPE
import timeit


class Java:
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
        print(f"Error getting version for {file_path}: {e}")
    return ""

def find_java_directories(base_path, match_keywords, exclude_keywords):
    java_list = []
    try:
        for root, dirs, files in os.walk(base_path):
            for dir_name in dirs:
                if any(exclude in dir_name for exclude in exclude_keywords):
                    continue
                if any(keyword in dir_name.lower() for keyword in match_keywords):
                    java_path = os.path.join(root, dir_name, 'bin', 'java.exe' if "windows" in system().lower() else 'java')
                    if os.path.isfile(java_path):
                        version = get_java_version(java_path)
                        if version:
                            java_list.append(Java(java_path, version))
    except Exception as e:
        print(f"Error searching directory {base_path}: {e}")
    print(java_list)
    return java_list

def detect_java_paths(start_paths, match_keywords, exclude_keywords, num_threads=10):
    java_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_path = {executor.submit(find_java_directories, path, match_keywords, exclude_keywords): path for path in start_paths}
        for future in concurrent.futures.as_completed(future_to_path):
            java_list.extend(future.result())
    return java_list

# 使用示例
match_keywords = [
    '1.', 'bin', 'cache', 'client', 'craft', 'data', 'download', 'eclipse', 'mine', 'mc', 'launch',
    'hotspot', 'java', 'jdk', 'jre', 'zulu', 'dragonwell', 'jvm', 'microsoft', 'corretto',
    'mod', 'mojang', 'net', 'netease', 'forge', 'liteloader', 'fabric', 'game', 'vanilla',
    'optifine', 'oracle', 'path', 'program', 'roaming', 'run', 'runtime', 'server', 'software',
    'temp', 'users', 'x64', 'x86', 'lib', 'usr', 'env', 'ext', 'file', 'data',
    '我的', '世界', '前置', '原版', '启动', '国服', '官启', '官方', '客户', '应用', '整合',
    os.getlogin(), '新建文件夹', '服务', '游戏', '环境', '程序', '网易', '软件', '运行', '高清',
    'badlion', 'blc', 'lunar', 'tlauncher', 'cb', 'cheatbreaker', 'hmcl', 'pcl', 'bakaxl', 'fsm'
]
exclude_keywords = ["$", "{", "}", "__"]

if system().lower() == "windows":
    start_paths = [f"{chr(i)}:\\" for i in range(65, 91) if os.path.exists(f"{chr(i)}:\\")]
else:
    start_paths = ["/usr", "/usr/java", "/usr/lib/jvm", "/usr/lib64/jvm", "/opt/jdk", "/opt/jdks"]

print(timeit.timeit(lambda: detect_java_paths(start_paths, match_keywords, exclude_keywords, num_threads=30), number=1))
