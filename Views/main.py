# coding:utf-8
import subprocess
import time

from PyQt5.QtCore import Qt, QEventLoop, QTimer, QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QSizePolicy
from qfluentwidgets import NavigationItemPosition, SplitFluentWindow, SubtitleLabel, setFont, NavigationInterface, \
    FluentWindow, SplashScreen, FluentStyleSheet, isDarkTheme, setTheme, Theme
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import TitleBar

from Helpers.Config import cfg
from Helpers.downloadHelper import download
from Helpers.getValue import ARIA2C_PATH, RPC_PORT
from Helpers.styleHelper import style_path
from Interfaces.DownloadInterfaces.DownloadInterface import DownloadInterface
from Interfaces.MainInterface import MainInterface
from Interfaces.VersionsInterfaces.VersionListsInterface import VersionListInterface
from Interfaces.SettingsInterfaces.SettingsInterface import SettingsInterface
from Interfaces.AccountInterface import AccountInterface
from Interfaces.activityInterface import activityInterface


class SplitTitleBar(TitleBar):

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 12)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.titleLabel.setObjectName('titleLabel')
        self.tipLabel = QLabel(self)
        self.tipLabel.setObjectName('tipLabel')
        self.tipLabel.setText("Beta")
        self.tipLabel.setStyleSheet('''
            color: #30d5c8;
            background: transparent;
            font: 13px 'Segoe UI';
            padding: 0 10px
    ''')
        self.hBoxLayout.insertWidget(3, self.tipLabel, 0, Qt.AlignLeft | Qt.AlignBottom)

        self.window().windowTitleChanged.connect(self.setTitle)

        FluentStyleSheet.FLUENT_WINDOW.apply(self)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))


class Window(SplitFluentWindow):

    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setQss()
        self.setTitleBar(SplitTitleBar(self))

        command = [
            ARIA2C_PATH,
            '--enable-rpc',
            '--rpc-listen-all=true',
            '--rpc-allow-origin-all',
            '--rpc-listen-port', str(RPC_PORT),
            '--max-concurrent-downloads=5',  #
            '--split=5',
            '--min-split-size=1M'
        ]
        # self.aria2c_process = subprocess.Popen(command)  # 把Aria2c启动
        if cfg.source.value == "官方":
            url = "http://launchermeta.mojang.com/mc/game/version_manifest.json"
        else:
            url = "https://bmclapi2.bangbang93.com/mc/game/version_manifest.json"
        # download(url, "cache")

        # create sub interface
        self.HomeInterface = MainInterface()
        self.VersionsListInterface = VersionListInterface()
        self.SettingsInterface = SettingsInterface()
        self.AccountInterface = AccountInterface()
        self.activityInterface = activityInterface()
        self.DownloadInterface = DownloadInterface()
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
        self.addSubInterface(self.HomeInterface, FIF.HOME, self.tr('主页'))
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.VersionsListInterface, FIF.BOOK_SHELF, self.tr('版本列表'))
        self.addSubInterface(self.activityInterface, FIF.TILES, self.tr('任务'))
        self.addSubInterface(self.DownloadInterface, FIF.DOWNLOAD, self.tr('下载'))
        self.addSubInterface(self.AccountInterface, FIF.PEOPLE, self.tr('游戏账号'), NavigationItemPosition.BOTTOM)
        self.navigationInterface.addSeparator(NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.SettingsInterface, FIF.SETTING, self.tr('设置'), NavigationItemPosition.BOTTOM)

        # NOTE: enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)

    def initWindow(self):
        self.resize(1200, 750)
        self.setWindowIcon(QIcon('resource/image/logo.png'))
        self.setWindowTitle('Python Minecraft Launcher')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def closeEvent(self, event):
        self.aria2c_process.terminate()
        self.aria2c_process.wait()
        event.accept()

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())
