# coding:utf-8

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import NavigationItemPosition,  SplitFluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF

from Interfaces.MainInterface import MainInterface
from Interfaces.VersionListsInterface import VersionListInterface
from Interfaces.SettingsInterfaces.SettingsInterface import SettingsInterface

class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

        # !IMPORTANT: leave some space for title bar
        self.hBoxLayout.setContentsMargins(0, 32, 0, 0)


class Window(SplitFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.HomeInterface = MainInterface()
        self.VersionsListInterface = VersionListInterface()
        self.SettingsInterface = SettingsInterface()

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.HomeInterface, FIF.HOME, '主页')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.VersionsListInterface, FIF.BOOK_SHELF, '版本列表')
        self.addSubInterface(self.SettingsInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)

        # NOTE: enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)

    def initWindow(self):
        self.resize(1600, 900)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('Python Minecraft Launcher Beta')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
