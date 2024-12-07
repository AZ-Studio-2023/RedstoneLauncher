# coding:utf-8
import os
from pathlib import Path
from time import ctime

from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QApplication, QFrame, QWidget, QStackedWidget, QSizePolicy

from qfluentwidgets import (NavigationBar, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor, SearchLineEdit,
                            PopUpAniStackedWidget, getFont, BreadcrumbBar, SubtitleLabel, setFont, ScrollArea,
                            HeaderCardWidget, BodyLabel, IconWidget, InfoBarIcon, ElevatedCardWidget, ImageLabel,
                            CaptionLabel, FlowLayout, GroupHeaderCardWidget, PushButton)
from qfluentwidgets import FluentIcon as FIF

from Helpers.Config import cfg
from Helpers.StartHelper import getAllVersion
from Helpers.getValue import COMMAND_PATH, FORGE_ICON, FABRIC_ICON, MINECRAFT_ICON, SAVES, SCREENSHOT, RES, MODS, \
    ROCKET, JOYSTICK
from Helpers.styleHelper import style_path
from Interfaces.VersionsInterfaces.ModsInterface import ModsInterface

ver = ""

def find_type(dictionary_list, key, value):
    for dictionary in dictionary_list:
        if key in dictionary and dictionary[key] == value:
            return dictionary["type"]
    return None
class FolderCard(GroupHeaderCardWidget):

    def __init__(self, parent=None):
        global ver
        super().__init__(parent)
        self.setTitle("文件夹")
        self.setBorderRadius(8)

        self.saves = PushButton("打开", self)
        self.screenshot = PushButton("打开", self)
        self.res = PushButton("打开", self)
        self.mod = PushButton("打开", self)


        self.addGroup(SAVES, "存档文件夹", "一键打开存档文件夹", self.saves)
        self.addGroup(SCREENSHOT, "截图文件夹", "一键打开截图文件夹", self.screenshot)
        self.addGroup(RES, "资源包文件夹", "一键打开资源包文件夹", self.res)
        if find_type(getAllVersion(cfg.gamePath.value), "name", ver) == "Forge" or find_type(getAllVersion(cfg.gamePath.value), "name", ver) == "Fabric":
            self.addGroup(MODS, "模组文件夹", "一键打开模组文件夹", self.mod)
        else:
            self.mod.setHidden(True)
        self.setFixedWidth(450)

class OthersCard(GroupHeaderCardWidget):

    def __init__(self, parent=None):
        global ver
        super().__init__(parent)
        self.setTitle("快捷操作")
        self.setBorderRadius(8)

        self.launch = PushButton("启动", self)
        self.out = PushButton("导出", self)

        self.addGroup(ROCKET, "一键启动", "一键启动该版本游戏", self.launch)
        self.addGroup(JOYSTICK, "导出启动脚本", "一键导出该版本游戏启动脚本", self.out)
        self.setFixedWidth(550)
class ImageCard(ElevatedCardWidget):

    def __init__(self, iconPath: str, name: str, parent=None):
        super().__init__(parent)
        self.iconWidget = ImageLabel(iconPath, self)
        self.label = CaptionLabel(name, self)

        self.iconWidget.scaledToHeight(68)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignHCenter | Qt.AlignBottom)

        self.setFixedSize(200, 250)


class GameInfoCard(HeaderCardWidget):
    """ Info Card """

    def __init__(self, version, parent=None):
        global ver
        super().__init__(parent)
        self.setTitle('概览')
        ver = version
        self.infoIcon = IconWidget(FIF.INFO, self)
        self.infoIcon1 = IconWidget(FIF.INFO, self)
        self.infoIcon2 = IconWidget(FIF.INFO, self)
        self.nameLabel = BodyLabel(f'版本名：{version}', self)
        self.typeLabel = BodyLabel(f'版本类型：{find_type(getAllVersion(cfg.gamePath.value), "name", version)}', self)
        if os.path.exists(os.path.join(COMMAND_PATH, f"{version}.bat")):
            self.timeLabel = BodyLabel(f'上次启动时间：{ctime(Path(os.path.join(COMMAND_PATH, f"{version}.bat")).stat().st_mtime)}', self)
        else:
            self.timeLabel = BodyLabel(
                '上次启动时间：从未启动', self)
        self.vBoxLayout = QVBoxLayout()
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout1 = QHBoxLayout()
        self.hBoxLayout2 = QHBoxLayout()


        self.infoIcon.setFixedSize(16, 16)
        self.infoIcon2.setFixedSize(16, 16)
        self.infoIcon1.setFixedSize(16, 16)

        self.hBoxLayout.setSpacing(10)
        self.hBoxLayout1.setSpacing(10)
        self.hBoxLayout2.setSpacing(10)

        self.vBoxLayout.setSpacing(16)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout1.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout2.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.hBoxLayout.addWidget(self.infoIcon)
        self.hBoxLayout.addWidget(self.nameLabel)
        self.hBoxLayout1.addWidget(self.infoIcon1)
        self.hBoxLayout1.addWidget(self.typeLabel)
        self.hBoxLayout2.addWidget(self.infoIcon2)
        self.hBoxLayout2.addWidget(self.timeLabel)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addLayout(self.hBoxLayout1)
        self.vBoxLayout.addLayout(self.hBoxLayout2)

        self.viewLayout.addLayout(self.vBoxLayout)


class VersionTemplateInterface(ScrollArea):

    def __init__(self, version, f, parent=None):
        super().__init__()
        self.setObjectName("VersionTemplate")
        self.f = f
        self.p = parent
        self.Layout = FlowLayout(self)
        self.info = GameInfoCard(version, self)
        self.info.setContentsMargins(0,0,0,0)
        self.Layout.addWidget(self.info)
        if find_type(getAllVersion(cfg.gamePath.value), "name", version) == "Forge":
            self.mod = ImageCard(FORGE_ICON, "模组管理")
            self.mod.clicked.connect(lambda: self.f(ModsInterface(version, self.f, self.p), "模组管理"))
        elif find_type(getAllVersion(cfg.gamePath.value), "name", version) == "Fabric":
            self.mod = ImageCard(FABRIC_ICON, "模组管理")
            self.mod.clicked.connect(lambda: self.f(ModsInterface(version, self.f, self.p), "模组管理"))
        else:
            self.mod = ImageCard(MINECRAFT_ICON, "原版客户端")
        self.mod.setContentsMargins(0, 0, 0, 0)
        self.Layout.addWidget(self.mod)
        self.folder = FolderCard(self)
        self.Layout.addWidget(self.folder)
        self.others = OthersCard(self)
        self.Layout.addWidget(self.others)
        self.setQss()
    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())