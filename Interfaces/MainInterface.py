# coding:utf-8
import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QApplication
from Helpers.getValue import MINECRAFT_ICON, FORGE_ICON, FABRIC_ICON
from qfluentwidgets import SwitchButton, SplitPushButton, FluentIcon, Action, RoundMenu, VBoxLayout, DropDownPushButton, \
    PushButton, TransparentPushButton, HorizontalFlipView, HorizontalPipsPager, LargeTitleLabel, TitleLabel, \
    TransparentDropDownPushButton, PrimaryPushButton
from PyQt5.QtGui import QIcon, QFont
from Helpers.Config import cfg
from Helpers.StartHelper import getAllVersion

class MainInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MainInterface")
        self.mainLayout = VBoxLayout(self)
        self.flipView = HorizontalFlipView()
        self.mainLayout.addWidget(self.flipView, alignment=Qt.AlignCenter)
        self.flipView.addImages(self.get_all_news())
        self.flipView.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.flipView.setFixedSize(QSize(1100, 450))
        self.flipView.setItemSize(QSize(1100, 450))
        self.flipView.setSpacing(15)
        self.flipView.setBorderRadius(15)
        self.pager = HorizontalPipsPager(self)
        self.mainLayout.addWidget(self.pager)
        self.pager.setPageNumber(self.flipView.count())
        self.pager.currentIndexChanged.connect(self.flipView.setCurrentIndex)
        self.flipView.currentIndexChanged.connect(self.pager.setCurrentIndex)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setAlignment(Qt.AlignBottom)
        self.bottomLayout.setContentsMargins(15, 0, 15, 15)
        self.mainLayout.addLayout(self.bottomLayout)


        self.startLayout = QVBoxLayout()
        self.accountButton = DropDownPushButton(FluentIcon.PEOPLE, self.tr(" 选择账号"))
        self.accountButton.setFixedSize(300, 60)
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
        self.start_button.setFixedSize(350,60)
        self.start_button.setText(self.tr("开始游戏"))
        self.startLayout.addWidget(self.start_button, alignment=Qt.AlignRight)
        self.bottomLayout.addLayout(self.startLayout)

    def setGameInfo(self, type, version):
        if type == "Vanilla":
            self.game_version_button.setIcon(QIcon(MINECRAFT_ICON))
        elif type == "Forge":
            self.game_version_button.setIcon(QIcon(FORGE_ICON))
        elif type == "Fabric":
            self.game_version_button.setIcon(QIcon(FABRIC_ICON))
        self.game_version_button.setText(str(version))
    def load_versions(self):
        versions = getAllVersion(cfg.gamePath.value)
        for ver in versions:
            if ver["type"] == "Vanilla":
                Vanilla_name = ver["name"]
                self.menu.addAction(
                    Action(QIcon(MINECRAFT_ICON), Vanilla_name, triggered=lambda: self.setGameInfo("Vanilla", Vanilla_name)))
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
