# coding:utf-8
import sys
from uuid import uuid1

from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QApplication, QFrame, QWidget, QStackedWidget

from qfluentwidgets import (NavigationBar, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor, SearchLineEdit,
                            PopUpAniStackedWidget, getFont, BreadcrumbBar, SubtitleLabel, setFont)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, TitleBar

from Helpers.Config import cfg
from Helpers.CustomControls import ListViewHelper
from Helpers.StartHelper import getAllVersion
from Helpers.styleHelper import style_path
from Helpers.getValue import MINECRAFT_ICON, FORGE_ICON, FABRIC_ICON
from Interfaces.DownloadInterfaces.checkInterface import checkInterface
from Interfaces.VersionsInterfaces.ModsInterface import ModsInterface
from Interfaces.VersionsInterfaces.VersionTemplateInterface import VersionTemplateInterface
from Interfaces.VersionsInterfaces.VersionListsInterface import VersionListInterface


class VersionInterface(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet('Demo{background:rgb(255,255,255)}')
        self.setObjectName("VersionInterface")
        self.breadcrumbBar = BreadcrumbBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.breadcrumbBar.currentItemChanged.connect(self.switchInterface)
        setFont(self.breadcrumbBar, 22)
        self.breadcrumbBar.setSpacing(20)

        self.addInterface(VersionListInterface(self.addInterface, self), "版本管理")

        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.addWidget(self.breadcrumbBar)
        self.vBoxLayout.addWidget(self.stackedWidget)

    def addInterface(self, interface, text: str):
        if not text:
            return

        w = interface
        w.setObjectName(text + "-" + str(uuid1().hex))

        self.stackedWidget.addWidget(w)
        self.stackedWidget.setCurrentWidget(w)

        self.breadcrumbBar.addItem(w.objectName(), text)

    def switchInterface(self, objectName):
        if "版本管理" in objectName:
            self.stackedWidget.setCurrentWidget(self.findChild(VersionListInterface, objectName))
        elif "模组管理" in objectName:
            self.stackedWidget.setCurrentWidget(self.findChild(ModsInterface, objectName))
        else:
            self.stackedWidget.setCurrentWidget(self.findChild(VersionTemplateInterface, objectName))

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

