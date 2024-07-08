# coding:utf-8
import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QApplication
from Helpers.getValue import MINECRAFT_ICON, FORGE_ICON, FABRIC_ICON
from qfluentwidgets import SwitchButton, SplitPushButton, FluentIcon, Action, RoundMenu, VBoxLayout, DropDownPushButton, \
    PushButton, TransparentPushButton, HorizontalFlipView, HorizontalPipsPager, LargeTitleLabel, TitleLabel, \
    TransparentDropDownPushButton, PrimaryPushButton
from PyQt5.QtGui import QIcon, QFont


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
        self.accountButton = DropDownPushButton(FluentIcon.PEOPLE, " 选择账号")
        self.accountButton.setFixedSize(300, 60)
        self.startLayout.addWidget(self.accountButton, alignment=Qt.AlignRight)
        # self.chose_button.setFont(self.font)
        self.game_version_button = DropDownPushButton(FluentIcon.PLAY, '选择游戏版本')
        # self.startLayout.addWidget(self.chose_button, alignment=Qt.AlignRight)
        self.startLayout.addWidget(self.game_version_button, alignment=Qt.AlignRight)
        self.game_version_button.setFixedSize(325, 60)
        self.menu = RoundMenu(parent=self.game_version_button)
        self.menu.addAction(
            Action(QIcon(MINECRAFT_ICON), '1.19', triggered=lambda: self.setGameInfo("Vanilla", "1.19")))
        self.menu.addAction(
            Action(QIcon(FORGE_ICON), '1.19 Forge', triggered=lambda: self.setGameInfo("Forge", "1.19 Forge")))
        self.menu.addAction(
            Action(QIcon(FABRIC_ICON), '1.19 Fabric', triggered=lambda: self.setGameInfo("Fabric", "1.19 Fabric")))
        self.game_version_button.setMenu(self.menu)
        self.start_button = PrimaryPushButton()
        self.start_button.setFixedSize(350,60)
        self.start_button.setText("开始游戏")
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

    def get_all_news(self):
        image_extensions = ['.jpg', '.jpeg', '.png']
        image_files = []

        for root, _, files in os.walk("resource/news"):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    relative_path = os.path.relpath(os.path.join(root, file), "resource/news")
                    image_files.append(os.path.join("resource/news", relative_path))

        return image_files
