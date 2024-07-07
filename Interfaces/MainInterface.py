# coding:utf-8
from PyQt5.QtWidgets import QWidget
from helper.getValue import MINECRAFT_ICON, FORGE_ICON, FABRIC_ICON
from qfluentwidgets import SwitchButton, SplitPushButton, FluentIcon, Action, RoundMenu, VBoxLayout
from PyQt5.QtGui import QIcon


class MainInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MainInterface")
        self.mainLayout = VBoxLayout(self)
        self.start_button = SplitPushButton(FluentIcon.PLAY, '选择版本并启动')
        self.start_button.resize(200,100)
        self.menu = RoundMenu(parent=self.start_button)
        self.menu.addAction(Action(QIcon(MINECRAFT_ICON), '1.19', triggered=lambda: self.setGameInfo(MINECRAFT_ICON, "1.19")))
        self.menu.addAction(Action(QIcon(FORGE_ICON), '1.19 Forge', triggered=lambda: self.setGameInfo(FORGE_ICON, "1.19 Forge")))
        self.menu.addAction(Action(QIcon(FABRIC_ICON), '1.19 Fabric', triggered=lambda: self.setGameInfo(FABRIC_ICON, "1.19 Fabric")))
        self.start_button.setFlyout(self.menu)
        self.mainLayout.addWidget(self.start_button)

    def setGameInfo(self, icon, version):
        self.start_button.setIcon(QIcon(icon))
        self.start_button.setText(str(version))
