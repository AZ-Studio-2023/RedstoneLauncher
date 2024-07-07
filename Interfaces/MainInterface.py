# coding:utf-8
import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QApplication
from Helpers.getValue import MINECRAFT_ICON, FORGE_ICON, FABRIC_ICON
from qfluentwidgets import SwitchButton, SplitPushButton, FluentIcon, Action, RoundMenu, VBoxLayout, DropDownPushButton, \
    PushButton, TransparentPushButton, HorizontalFlipView
from PyQt5.QtGui import QIcon, QFont


class MainInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MainInterface")
        self.mainLayout = VBoxLayout(self)
        self.flipView = HorizontalFlipView()
        self.mainLayout.addWidget(self.flipView)
        self.flipView.addImages(self.get_all_news())
        self.flipView.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.flipView.setFixedSize(QSize(1200, 400))
        self.flipView.setItemSize(QSize(1200, 400))
        self.flipView.setSpacing(15)
        self.flipView.setBorderRadius(15)

        self.startLayout = QVBoxLayout()
        self.startLayout.setAlignment(Qt.AlignBottom)
        self.startLayout.setContentsMargins(0, 0, 30, 30)
        self.chose_button = TransparentPushButton()
        self.chose_button.setText("Please choose a Version.")
        self.font = QFont()
        self.font.setFamily("Microsoft YaHei")
        self.font.setPointSize(15)
        self.chose_button.setFont(self.font)
        self.start_button = PushButton(FluentIcon.PLAY, 'Start Minecraft!')
        self.startLayout.addWidget(self.chose_button, alignment=Qt.AlignRight)
        self.startLayout.addWidget(self.start_button, alignment=Qt.AlignRight)
        self.start_button.setFixedSize(175,80)
        self.menu = RoundMenu(parent=self.start_button)
        self.menu.addAction(Action(QIcon(MINECRAFT_ICON), '1.19', triggered=lambda: self.setGameInfo(MINECRAFT_ICON, "1.19")))
        self.menu.addAction(Action(QIcon(FORGE_ICON), '1.19 Forge', triggered=lambda: self.setGameInfo(FORGE_ICON, "1.19 Forge")))
        self.menu.addAction(Action(QIcon(FABRIC_ICON), '1.19 Fabric', triggered=lambda: self.setGameInfo(FABRIC_ICON, "1.19 Fabric")))
        # self.start_button.setMenu(self.menu)
        self.mainLayout.addLayout(self.startLayout)


    def setGameInfo(self, icon, version):
        self.start_button.setIcon(QIcon(icon))
        self.start_button.setText(str(version))

    def get_all_news(self):
        image_extensions = ['.jpg', '.jpeg', '.png']
        image_files = []

        for root, _, files in os.walk("resource/news"):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    relative_path = os.path.relpath(os.path.join(root, file), "resource/news")
                    image_files.append(os.path.join("resource/news", relative_path))

        return image_files
