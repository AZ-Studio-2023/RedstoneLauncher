# coding:utf-8
import os.path
import subprocess
import sys

import aria2p
from PyQt5.QtCore import Qt, QEventLoop, QTimer, QSize
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication, QLabel
from qfluentwidgets import NavigationItemPosition, SplitFluentWindow, SplashScreen, FluentStyleSheet
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import TitleBar

from Helpers.Config import cfg
from Helpers.getValue import ARIA2C_PATH, RPC_PORT, VERSION, UPDATE_NUMBER
from Helpers.pluginHelper import load_plugins, run_plugins
from Helpers.styleHelper import style_path
from Interfaces.DownloadInterfaces.downloadInterface import downloadInterface
from Interfaces.MainInterface import MainInterface
from Interfaces.VersionsInterfaces.VersionInterface import VersionInterface
from Interfaces.SettingsInterfaces.SettingsInterface import SettingsInterface
from Interfaces.AccountInterface import AccountInterface
from Interfaces.activityInterfaces.activityInterface import activityInterface
from Interfaces.plugin import plugins
from Helpers.outputHelper import logger

logger.info(f"Redstone Launcher  Ver.{VERSION}")
logger.info(f"更新序列号：{UPDATE_NUMBER}")
logger.debug("Debug模式：开")
logger.info(f"当前游戏目录：{cfg.gamePath.value}")


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
        font_id = QFontDatabase.addApplicationFont(os.path.join("resource", "font", "Minecraft_UTF-8.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.mc_font = QFont(font_family)
        self.titleLabel.setObjectName('titleLabel')
        self.tipLabel = QLabel(self)
        self.tipLabel.setObjectName('tipLabel')
        self.tipLabel.setText("Preview")
        self.tipLabel.setFont(self.mc_font)
        self.tipLabel.setStyleSheet('''
            color: #30d5c8;
            background: transparent;
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


        # create sub interface
        self.HomeInterface = MainInterface()
        self.VersionInterface = VersionInterface()
        self.SettingsInterface = SettingsInterface()
        self.AccountInterface = AccountInterface()
        self.activityInterface = activityInterface()
        self.downloadInterface = downloadInterface()
        self.pluginsInterface = plugins()
        self.stackedWidget.hBoxLayout.setContentsMargins(0, 40, 0, 0)
        self.initNavigation()
        self.initWindow()
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()
        self.createSubInterface()
        command = [
            ARIA2C_PATH,
            '--enable-rpc',
            '--rpc-listen-all=true',
            '--rpc-allow-origin-all',
            '--rpc-listen-port', str(RPC_PORT),
            '--max-concurrent-downloads=20',
            '--split=15',
            '--min-split-size=1M'
        ]
        self.aria2c_process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        if cfg.PluginEnable.value:
            load_plugins(parent=self)
            run_plugins(parent=self)
        self.splashScreen.finish()


    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(1500, loop.quit)
        loop.exec()

    def initNavigation(self):
        self.addSubInterface(self.HomeInterface, FIF.HOME, self.tr('主页'))
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.VersionInterface, FIF.BOOK_SHELF, self.tr('版本管理'))
        self.addSubInterface(self.activityInterface, FIF.TILES, self.tr('任务'))
        self.addSubInterface(self.downloadInterface, FIF.DOWNLOAD, self.tr('下载'))
        self.addSubInterface(self.AccountInterface, FIF.PEOPLE, self.tr('游戏账号'), NavigationItemPosition.BOTTOM)
        if cfg.PluginEnable.value:
            self.addSubInterface(self.pluginsInterface, FIF.APPLICATION, '插件', position=NavigationItemPosition.BOTTOM)
        self.navigationInterface.addSeparator(NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.SettingsInterface, FIF.SETTING, self.tr('设置'), NavigationItemPosition.BOTTOM)

        # NOTE: enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)

    def initWindow(self):
        self.setWindowIcon(QIcon('resource/image/logo.png'))
        self.setWindowTitle('Redstone Launcher')

        self.base_width = 1200
        self.base_height = 750

        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        screen_width = screen_size.width()
        screen_height = screen_size.height()
        scale_factor = min(screen_width / self.base_width, screen_height / self.base_height)
        new_width = int(self.base_width * scale_factor)
        new_height = int(self.base_height * scale_factor)
        new_width = min(new_width, self.base_width)
        new_height = min(new_height, self.base_height)
        self.resize(new_width, new_height)
        self.move((screen_width - new_width) // 2, (screen_height - new_height) // 2)

    def closeEvent(self, event):
        self.aria2c_process.terminate()
        self.aria2c_process.wait()
        event.accept()
        sys.exit()

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())
