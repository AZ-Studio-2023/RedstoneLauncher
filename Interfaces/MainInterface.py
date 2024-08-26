# coding:utf-8
import json
import os
import random
import uuid

import psutil
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QApplication, QSizePolicy, QLabel
from qfluentwidgets.components.widgets.acrylic_label import AcrylicLabel

from Helpers.flyoutmsg import dlerr, dlsuc, dlwar
from Helpers.getValue import MINECRAFT_ICON, FORGE_ICON, FABRIC_ICON, MICROSOFT_ACCOUNT, LEGACY_ACCOUNT, \
    THIRD_PARTY_ACCOUNT, setLaunchData
from qfluentwidgets import SwitchButton, SplitPushButton, FluentIcon, Action, RoundMenu, VBoxLayout, DropDownPushButton, \
    PushButton, TransparentPushButton, HorizontalFlipView, HorizontalPipsPager, LargeTitleLabel, TitleLabel, \
    TransparentDropDownPushButton, PrimaryPushButton, ImageLabel
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QColor
from Helpers.Config import cfg
from Helpers.StartHelper import getAllVersion, launch, getVersionType, getVersionInfo
from Helpers.getValue import setProcessData, getProcessData

version_chose = False
account_chose = False
account_list = []

def find_dict(dictionary_list, key, value):
    for dictionary in dictionary_list:
        if key in dictionary and dictionary[key] == value:
            return dictionary
    return None

class MainInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MainInterface")
        self.mainLayout = VBoxLayout(self)

        self.mainImage = HorizontalFlipView(self)
        self.mainImage.addImages(self.get_all_news())
        self.mainLayout.addWidget(self.mainImage)
        self.mainImage.setSpacing(15)
        self.mainImage.setBorderRadius(15)
        self.mainImage.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.mainImage.setItemSize(QSize(1200, 450))
        self.mainImage.resize(QSize(1200, 450))
        self.mainImage.setFixedHeight(450)

        self.pager = HorizontalPipsPager(self)
        self.pager.setPageNumber(self.mainImage.count())
        self.pager.currentIndexChanged.connect(self.mainImage.setCurrentIndex)
        self.mainImage.currentIndexChanged.connect(self.pager.setCurrentIndex)
        self.mainLayout.addWidget(self.pager)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setAlignment(Qt.AlignBottom)
        self.bottomLayout.setContentsMargins(15, 0, 15, 15)
        self.mainLayout.addLayout(self.bottomLayout)

        self.startLayout = QVBoxLayout()
        self.accountButton = DropDownPushButton(FluentIcon.PEOPLE, self.tr(" 选择账号"))
        self.accountButton.clicked.connect(self.load_account)
        self.accountButton.setFixedSize(300, 60)
        self.account_menu = RoundMenu(parent=self.accountButton)
        self.accountButton.setMenu(self.account_menu)
        self.startLayout.addWidget(self.accountButton, alignment=Qt.AlignRight)
        # self.chose_button.setFont(self.font)
        self.game_version_button = DropDownPushButton(FluentIcon.PLAY, self.tr('选择游戏版本'))
        # self.startLayout.addWidget(self.chose_button, alignment=Qt.AlignRight)
        self.startLayout.addWidget(self.game_version_button, alignment=Qt.AlignRight)
        self.game_version_button.setFixedSize(325, 60)
        self.menu = RoundMenu(parent=self.game_version_button)
        self.load_versions()
        self.game_version_button.setMenu(self.menu)
        self.start_button = PrimaryPushButton()
        self.start_button.setFixedSize(350, 60)
        self.start_button.setText(self.tr("开始游戏"))
        self.start_button.clicked.connect(self.start_game)
        self.startLayout.addWidget(self.start_button, alignment=Qt.AlignRight)
        self.bottomLayout.addLayout(self.startLayout)

        self.launch_worker = launch()
        self.launch_worker.finished.connect(self.launch_finish)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_image)
        self.timer.start(10000)

    def next_image(self):
        if self.mainImage.count() == self.mainImage.currentIndex()+1:
            self.mainImage.setCurrentIndex(0)
        else:
            self.mainImage.setCurrentIndex(self.mainImage.currentIndex()+1)

    def launch_start(self):
        mem = psutil.virtual_memory()
        launch_uuid = str(uuid.uuid4())
        data = getProcessData()
        data.append({"uuid": launch_uuid, "state": "未知", "logger": "", "version": self.game_version_button.text()})
        setProcessData(data)
        free_memory = mem.available
        free_memory_mb = free_memory / 1024 / 1024
        free_memory_mb = int(free_memory_mb) * 0.8
        f = open(os.path.join("data", "accounts.json"), "r")
        account_data = json.loads(f.read())
        f.close()
        launch_data = {
            "javaDir": cfg.javaPath.value,
            "gameDir": cfg.gamePath.value, "clientVersion": getVersionInfo(cfg.gamePath.value, self.game_version_button.text())["clientVersion"], "xmx": free_memory_mb,
            "gameType": getVersionType(cfg.gamePath.value, self.game_version_button.text()), "userType": "Legacy",
            "uuid": find_dict(account_data["accounts"], "name", self.accountButton.text())["uuid"], "accessToken": "", "versionType": getVersionInfo(cfg.gamePath.value, self.game_version_button.text())["type"],
            "username": self.accountButton.text(), "version": self.game_version_button.text(), "process_uuid": launch_uuid}
        setLaunchData(launch_data)
        dlsuc(self, "游戏进程启动中！可前往任务页查看详细信息")
        self.launch_worker.start()

    def launch_finish(self, return_data):
        if return_data["state"] == "0":
            dic = find_dict(getProcessData(), "uuid", return_data["uuid"])
            data = getProcessData()
            data.remove(dic)
            data.append({"uuid": return_data["uuid"], "state": "补全游戏所需资源", "logger": "",
                         "version": self.game_version_button.text(), "code": 0})
            setProcessData(data)
        elif return_data["state"] == "1":
            dic = find_dict(getProcessData(), "uuid", return_data["uuid"])
            data = getProcessData()
            data.remove(dic)
            data.append({"uuid": return_data["uuid"], "state": "构建启动命令", "logger": "",
                         "version": self.game_version_button.text(), "code": 1})
            setProcessData(data)
        elif return_data["state"] == "2":
            dic = find_dict(getProcessData(), "uuid", return_data["uuid"])
            data = getProcessData()
            data.remove(dic)
            data.append({"uuid": return_data["uuid"], "state": "游戏进程已启动", "logger": "",
                         "version": self.game_version_button.text(), "code": 2})
            setProcessData(data)
        elif return_data["state"] == "3":
            dic = find_dict(getProcessData(), "uuid", return_data["uuid"])
            data = getProcessData()
            data.remove(dic)
            data.append({"uuid": return_data["uuid"], "state": "游戏进程已退出", "logger": "",
                         "version": self.game_version_button.text(), "code": 3})
            setProcessData(data)
            self.launch_worker.quit()

    def setGameInfo(self, type, version):
        global version_chose
        if type == "Vanilla":
            self.game_version_button.setIcon(QIcon(MINECRAFT_ICON))
        elif type == "Forge":
            self.game_version_button.setIcon(QIcon(FORGE_ICON))
        elif type == "Fabric":
            self.game_version_button.setIcon(QIcon(FABRIC_ICON))
        self.game_version_button.setText(str(version))
        version_chose = True

    def setAccountInfo(self, type, name):
        global account_chose
        if type == "Microsoft":
            self.accountButton.setIcon(QIcon(MICROSOFT_ACCOUNT))
        elif type == "Legacy":
            self.accountButton.setIcon(QIcon(LEGACY_ACCOUNT))
        elif type == "Third-Party":
            self.accountButton.setIcon(QIcon(THIRD_PARTY_ACCOUNT))
        self.accountButton.setText(str(name))
        account_chose = True

    def load_account(self):
        global account_list
        f = open("data/accounts.json", "r")
        data = json.loads(f.read())["accounts"]
        f.close()
        items_to_remove = []

        for item in account_list:
            self.account_menu.removeAction(item)
            items_to_remove.append(item)

        for item in items_to_remove:
            account_list.remove(item)

        for account in data:
            if account["type"] == "Microsoft":
                action = Action(QIcon(MICROSOFT_ACCOUNT), account["name"],
                           triggered=self.create_lambda("Microsoft", account["name"]))
                self.account_menu.addAction(action)
                account_list.append(action)
            elif account["type"] == "Legacy":
                action = Action(QIcon(LEGACY_ACCOUNT), account["name"],
                           triggered=self.create_lambda("Legacy", account["name"]))
                self.account_menu.addAction(action)
                account_list.append(action)
            else:
                action = Action(QIcon(THIRD_PARTY_ACCOUNT), account["name"],
                           triggered=self.create_lambda("Third-Party", account["name"]))
                self.account_menu.addAction(action)
                account_list.append(action)

    def create_lambda(self, account_type, account_name):
        def lambda_function():
            self.setAccountInfo(account_type, account_name)

        return lambda_function

    def start_game(self):
        global version_chose
        global account_chose
        if version_chose and account_chose:
            if cfg.javaPath.value != "":
                self.launch_start()
            else:
                dlerr(self.tr("无可用Java运行时，请先前往设置中进行配置"), self)
        else:
            dlerr(self.tr("未选择游戏版本或游戏账户"), self)

    def load_versions(self):
        versions = getAllVersion(cfg.gamePath.value)
        for ver in versions:
            if ver["type"] == "Vanilla":
                Vanilla_name = ver["name"]
                self.menu.addAction(
                    Action(QIcon(MINECRAFT_ICON), Vanilla_name,
                           triggered=lambda: self.setGameInfo("Vanilla", Vanilla_name)))
            elif ver["type"] == "Forge":
                Forge_name = ver["name"]
                self.menu.addAction(
                    Action(QIcon(FORGE_ICON), Forge_name, triggered=lambda: self.setGameInfo("Forge", Forge_name)))
            else:
                Fabric_name = ver["name"]
                self.menu.addAction(
                    Action(QIcon(FABRIC_ICON), Fabric_name, triggered=lambda: self.setGameInfo("Fabric", Fabric_name)))

    def get_all_news(self):
        image_extensions = ['.jpg', '.jpeg', '.png']
        image_files = []

        for root, _, files in os.walk("resource/news"):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    relative_path = os.path.relpath(os.path.join(root, file), "resource/news")
                    image_files.append(os.path.join("resource/news", relative_path))

        return image_files
