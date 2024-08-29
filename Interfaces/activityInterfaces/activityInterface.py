# coding:utf-8

from PyQt5.QtCore import pyqtSignal, QEasingCurve, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QWidget

from qfluentwidgets import (NavigationItemPosition, PopUpAniStackedWidget)
from qfluentwidgets import FluentIcon as FIF

import Helpers.StartHelper
from Interfaces.activityInterfaces.downloadActivityInterface import downloadActivityInterface
from Interfaces.activityInterfaces.loggerInterface import loggerInterface

from Helpers.Config import cfg
from Helpers.CustomControls import ListViewHelper
from Helpers.styleHelper import style_path
from Helpers.getValue import MINECRAFT_ICON, FORGE_ICON, FABRIC_ICON, getProcessData

local_process = []
local_process_data = {}


class StackedWidget(QFrame):
    """ Stacked widget """

    currentChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(self.currentChanged)

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def widget(self, index: int):
        return self.view.widget(index)

    def setCurrentWidget(self, widget, popOut=False):
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.InQuad)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class activityInterface(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("activityInterface")

        # use dark theme mode
        # setTheme(Theme.DARK)

        # change the theme color
        # setThemeColor('#0078d4')

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationBar = ListViewHelper(self)
        self.stackWidget = StackedWidget(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_process)
        self.timer.start(100)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()
        self.setQss()

    def initLayout(self):
        self.hBoxLayout.addWidget(self.navigationBar)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.addSubInterface(loggerInterface("tip", "tip"), FIF.INFO, "提示", "tip")
        self.addSubInterface(downloadActivityInterface(), FIF.DOWNLOAD, "下载任务", "download", position=NavigationItemPosition.BOTTOM)
        self.navigationBar.setCurrentItem("tip")
        self.stackWidget.setCurrentIndex(0)
        # hide the text of button when selected
        # self.navigationBar.setSelectedTextVisible(False)

        # adjust the font size of button
        # self.navigationBar.setFont(getFont(12))

    def addSubInterface(self, interface, icon, text: str, uuid, position=NavigationItemPosition.TOP, selectedIcon=None):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationBar.addItem(
            routeKey=uuid,
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            selectedIcon=selectedIcon,
            position=position,
        )

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationBar.setCurrentItem(widget.objectName())


    def change_process(self):
        global local_process
        global local_process_data
        data = getProcessData()
        for i in data:
            if i["uuid"] not in local_process:
                if Helpers.StartHelper.getVersionType(cfg.gamePath.value, i["version"]) == "Vanilla":
                    self.addSubInterface(loggerInterface(i["uuid"], i["version"]), QIcon(MINECRAFT_ICON), i["version"], i["uuid"])
                elif Helpers.StartHelper.getVersionType(cfg.gamePath.value, i["version"]) == "Forge":
                    self.addSubInterface(loggerInterface(i["uuid"], i["version"]), QIcon(FORGE_ICON),
                                             i["version"], i["uuid"])
                else:
                    self.addSubInterface(loggerInterface(i["uuid"], i["version"]), QIcon(FABRIC_ICON),
                                         i["version"], i["uuid"])
                local_process.append(i["uuid"])
                if len(local_process) == 1:
                    self.navigationBar.removeWidget("tip")
                self.navigationBar.setCurrentItem(i["uuid"])
                self.stackWidget.setCurrentIndex(len(local_process))
        self.repaint()
        self.update()
