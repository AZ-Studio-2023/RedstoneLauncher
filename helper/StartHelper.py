import os
import json
import subprocess
import zipfile
import platform


def decompression(filename: str, path: str):
    try:
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(path)
        return 0
    except FileNotFoundError:
        return "Error"


def start(javaDir, gameDir, version, xmx, gameType, username, uuid, accessToken, userType, versionType):
    if gameType == "vanilla":  # 判断客户端类型
        main_class = "net.minecraft.client.main.Main"
    else:
        main_class = "net.minecraft.launchwrapper.Launch"
    pc_os = platform.system()
    assetsDir = os.path.join(gameDir, "assets")
    assetIndex = version
    native_library = str(os.path.join(gameDir, "versions", version, f"{version}-natives"))

    native_list = []
    native_list.append(os.path.join(gameDir, "versions", version, f"{version}.jar"))
    version_path = os.path.join(gameDir, "versions", version, f"{version}.json")
    version_json = open(version_path, "r")
    version_data = json.loads(version_json.read())
    for libraries in version_data["libraries"]:
        for native in libraries["downloads"]:
            if native == "artifact":
                dirct_path = native_library
                file_path = str(
                    os.path.normpath(os.path.join(gameDir, "libraries", libraries["downloads"][native]['path'])))
                if not os.path.exists(f"{version}.bat"):
                    if decompression(file_path, dirct_path) == 0:
                        native_list.append(file_path)
                else:
                    native_list.append(file_path)
            elif native == 'classifiers':
                for n in libraries['downloads'][native].values():
                    dirct_path = str(os.path.join(gameDir, "libraries", libraries["downloads"][native]['path']))
                    file_path = str(os.path.join(gameDir, "libraries", n["path"]))
                    if not os.path.exists(f"{version}.bat"):
                        decompression(file_path, dirct_path)

    # 构建本地库字符串
    if pc_os == "Windows":
        cp = ';'.join(native_list)
    else:
        cp = ':'.join(native_list)
    #构建启动命令
    jvm_args = [
        f"-Xmx{xmx}m",
        "-Xmn128m",
        "-XX:+UseG1GC",
        "-XX:-UseAdaptiveSizePolicy",
        "-XX:-OmitStackTraceInFastThrow",
        f"-Djava.library.path={native_library}",
        f"-Dminecraft.launcher.brand=Python Minecraft Launcher",
        f"-Dminecraft.launcher.version=0.9.6",
        "-cp",
        f"{cp}"
    ]
    # mc_args = [
    #     main_class,
    #     f"--username {username}",
    #     f"--version {version}",
    #     f"--gameDir {gameDir}",
    #     f"--assetsDir {assetsDir}",
    #     f"--assetIndex {assetIndex}",
    #     f"--uuid {uuid}",
    #     f"--accessToken {accessToken}",
    #     f"--userType {userType}",
    #     f"--versionType {versionType}"
    # ]
    mc_args = [
        main_class,
        "--username", username,
        "--version", version,
        "--gameDir", gameDir,
        "--assetsDir", assetsDir,
        "--assetIndex", assetIndex,
        "--uuid", uuid,
        "--accessToken", accessToken,
        "--userType", userType,
        "--versionType", versionType
    ]
    command = [javaDir] + jvm_args + mc_args
    u = open(f"{version}.bat", "w")
    u.write(str(command))
    u.close()
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode('utf-8'))
    print(result.stderr.decode('utf-8'))


start(javaDir="C:\\Users\\18079\AppData\Roaming\.minecraft\\runtime\java-runtime-gamma-snapshot\\bin\javaw.exe",
      gameDir="C:\\Users\\18079\Documents\PCL2\.minecraft",
      version="1.19",
      xmx=1024,
      gameType="vanilla",
      userType="msa",
      uuid="d9e667e2dbf446568f3f8875f89447a3",
      accessToken="eyJraWQiOiJhYzg0YSIsImFsZyI6IkhTMjU2In0.eyJ4dWlkIjoiMjUzNTQ2Mzg2MDcxNDQ5NyIsImFnZyI6IkFkdWx0Iiwic3ViIjoiZmU1NWNkMjEtNjRjYy00NGJlLWE2ZTQtYzJkN2E5OWFmZjA1IiwiYXV0aCI6IlhCT1giLCJucyI6ImRlZmF1bHQiLCJyb2xlcyI6W10sImlzcyI6ImF1dGhlbnRpY2F0aW9uIiwiZmxhZ3MiOlsidHdvZmFjdG9yYXV0aCIsIm1zYW1pZ3JhdGlvbl9zdGFnZTQiLCJvcmRlcnNfMjAyMiIsIm11bHRpcGxheWVyIl0sInByb2ZpbGVzIjp7Im1jIjoiZDllNjY3ZTItZGJmNC00NjU2LThmM2YtODg3NWY4OTQ0N2EzIn0sInBsYXRmb3JtIjoiVU5LTk9XTiIsInl1aWQiOiI3MTNhODZlMGY0MTVmODljMzM2MGVhYmY2ZTlmM2M2OSIsIm5iZiI6MTcyMDI1MDAxMywiZXhwIjoxNzIwMzM2NDEzLCJpYXQiOjE3MjAyNTAwMTN9.WHi8FtGrNj1a7SYg9m5tfMOTGkWPO-tEYHenAwgh-UE",
      versionType="Test",
      username="zenglingkun1125"
      )
