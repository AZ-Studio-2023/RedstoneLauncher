# coding:utf-8
import json
import os
import random

from PyQt5.QtCore import Qt, QSize
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
from Helpers.StartHelper import getAllVersion, launch, getVersionType

status = False
version_chose = False
account_chose = False


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
        self.load_account()
        self.game_version_button.setMenu(self.menu)
        self.start_button = PrimaryPushButton()
        self.start_button.setFixedSize(350, 60)
        self.start_button.setText(self.tr("开始游戏"))
        self.start_button.clicked.connect(self.start_game)
        self.startLayout.addWidget(self.start_button, alignment=Qt.AlignRight)
        self.bottomLayout.addLayout(self.startLayout)

        self.launch_worker = launch()
        self.launch_worker.finished.connect(self.launch_finish)

    def launch_start(self):
        global status
        status = True
        launch_data = {
            "javaDir": "C:\\Users\\18079\AppData\Roaming\.minecraft\\runtime\java-runtime-gamma-snapshot\\bin\javaw.exe",
            "gameDir": cfg.gamePath.value, "version": self.game_version_button.text(), "xmx": 1024,
            "gameType": getVersionType(cfg.gamePath.value, self.game_version_button.text()), "userType": "Legacy",
            "uuid": "", "accessToken": "", "versionType": "Python_Minecraft_Launcher",
            "username": self.accountButton.text()}
        setLaunchData(launch_data)
        self.launch_worker.start()

    def launch_finish(self, return_data):
        if return_data == "0":
            dlsuc(self, "获取参数完毕")
        elif return_data == "1":
            dlsuc(self, "本地库列表生成完毕")
        elif return_data == "2":
            dlsuc(self, "启动命令构建完毕，等待游戏窗口出现", show_time=10000)
        else:
            global status
            status = False
            self.launch_worker.quit()
            dlwar("游戏进程已结束", self, show_time=5000)

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
        f = open("data/accounts.json", "r")
        data = json.loads(f.read())["accounts"]
        f.close()
        for account in data:
            if account["type"] == "Microsoft":
                self.account_menu.addAction(
                    Action(QIcon(MICROSOFT_ACCOUNT), account["name"],
                           triggered=lambda: self.setAccountInfo("Microsoft", account["name"])))
            elif account["type"] == "Legacy":
                self.account_menu.addAction(
                    Action(QIcon(LEGACY_ACCOUNT), account["name"],
                           triggered=lambda: self.setAccountInfo("Legacy", account["name"])))
            else:
                self.account_menu.addAction(
                    Action(QIcon(THIRD_PARTY_ACCOUNT), account["name"],
                           triggered=lambda: self.setAccountInfo("Third-Party", account["name"])))

    def start_game(self):
        global status
        global version_chose
        global account_chose
        if version_chose and account_chose:
            if not status:
                self.launch_start()
            else:
                dlerr(self.tr("当前已有游戏进程启动"), self)
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
