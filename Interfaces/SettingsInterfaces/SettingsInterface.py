# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel

from qfluentwidgets import Pivot, setTheme, Theme

from .AboutSettingsInterface import AboutSettingsInterface
from .ApplicationSettingsInterface import AppilacationSettingsInterface
from .GameSettingsInterface import GameSettingsInterface


class SettingsInterface(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setObjectName("SettingsInterfaces")

        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.GameSettingsInterface = GameSettingsInterface()
        self.AppilacationSettingsInterface = AppilacationSettingsInterface()
        self.AboutSettingsInterface = AboutSettingsInterface()

        # add items to pivot
        self.addSubInterface(self.GameSettingsInterface, 'GameSettingsInterface', self.tr('游戏设置'))
        self.addSubInterface(self.AppilacationSettingsInterface, 'AppilacationSettingsInterface', self.tr('应用程序设置'))
        self.addSubInterface(self.AboutSettingsInterface, 'AboutSettingsInterface', self.tr('关于'))

        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 0, 30, 30)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.GameSettingsInterface)
        self.pivot.setCurrentItem(self.GameSettingsInterface.objectName())

    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())

