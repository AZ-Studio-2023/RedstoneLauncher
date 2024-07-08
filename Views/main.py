# coding:utf-8

from PyQt5.QtCore import Qt, QEventLoop, QTimer, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import NavigationItemPosition, SplitFluentWindow, SubtitleLabel, setFont, NavigationInterface, \
    FluentWindow, SplashScreen
from qfluentwidgets import FluentIcon as FIF

from Interfaces.MainInterface import MainInterface
from Interfaces.VersionsInterfaces.VersionListsInterface import VersionListInterface
from Interfaces.SettingsInterfaces.SettingsInterface import SettingsInterface


class Window(SplitFluentWindow):

    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")

        # create sub interface
        self.HomeInterface = MainInterface()
        self.VersionsListInterface = VersionListInterface()
        self.SettingsInterface = SettingsInterface()
        self.stackedWidget.hBoxLayout.setContentsMargins(0, 40, 0, 0)
        self.initNavigation()
        self.initWindow()
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()
        self.createSubInterface()
        self.splashScreen.finish()


    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(1500, loop.quit)
        loop.exec()

    def initNavigation(self):
        self.addSubInterface(self.HomeInterface, FIF.HOME, self.tr('Home Page'))
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.VersionsListInterface, FIF.BOOK_SHELF, self.tr('Versions List'))
        self.addSubInterface(self.SettingsInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

        # NOTE: enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)

    def initWindow(self):
        self.resize(1200, 750)
        self.setWindowIcon(QIcon('resource/image/logo.png'))
        self.setWindowTitle('Python Minecraft Launcher Beta')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def resizeEvent(self, event):
        new_size = event.size()
        if event.spontaneous():
            self.HomeInterface.flipView.setFixedWidth(new_size.width() - 100)
        super().resizeEvent(event)



