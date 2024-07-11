import os
import subprocess
from platform import system
from concurrent.futures import ThreadPoolExecutor, as_completed

# 关键词列表
keywords = [
    'java', 'jdk', 'jre'
]

def get_java_version(java_path):
    """
    获取Java版本信息。
    """
    try:
        result = subprocess.run([java_path, '-version'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        output = result.stderr
        version_line = output.split('\n')[0]
        version = version_line.split('"')[1]
        return version
    except Exception as e:
        print(f"Error getting version for {java_path}: {e}")
        return "Unknown"

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

def find_javaw(candidate_dirs):
    """
    在候选目录中查找javaw.exe文件，并返回包含路径和版本信息的字典列表。
    """
    java_list = []
    for dir_path in candidate_dirs:
        for root, _, files in os.walk(dir_path):
            if "javaw.exe" in files:
                java_path = os.path.join(root, "javaw.exe")
                version = get_java_version(java_path)
                java_list.append({"name": f"JDK {version}", "path": java_path})
    return java_list

def detect_all_javaw():
    """
    检测所有已安装的javaw.exe路径，并返回包含路径和版本信息的字典列表。
    """
    java_list = []
    futures = []
    max_workers = 8
    candidate_dirs = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        if system().lower() == 'windows':
            for drive in range(ord('C'), ord('Z') + 1):
                drive_path = f"{chr(drive)}:\\"
                if os.path.exists(drive_path):
                    futures.append(executor.submit(search_keywords, drive_path, keywords))
        else:
            # 假定在类Unix系统上
            default_paths = ["/usr", "/usr/lib", "/usr/local", "/opt"]
            for path in default_paths:
                if os.path.exists(path):
                    futures.append(executor.submit(search_keywords, path, keywords))

        for future in as_completed(futures):
            candidate_dirs.extend(future.result())

    # 使用多线程并行查找javaw.exe
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(find_javaw, [dir_path]) for dir_path in candidate_dirs]
        for future in as_completed(futures):
            java_list.extend(future.result())

    return java_list

# 调用检测函数并打印结果
java_installations = detect_all_javaw()
for java in java_installations:
    print(java)