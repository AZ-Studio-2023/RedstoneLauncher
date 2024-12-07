import json
import os.path

import requests
from PyQt5.QtCore import Qt, QThreadPool, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QHBoxLayout, QVBoxLayout, QAbstractItemView, QTableWidgetItem, \
    QTableView
from qfluentwidgets import FluentIcon, ExpandGroupSettingCard, SubtitleLabel, PrimaryPushButton, PushButton, ScrollArea, \
    VBoxLayout, SettingCardGroup, isDarkTheme, IconWidget, CardWidget, CaptionLabel, BodyLabel, TransparentToolButton, \
    IndeterminateProgressBar, OptionsSettingCard, ListWidget, TableWidget, CommandBarView, Action, Flyout, \
    FlyoutAnimationType, CommandBar, RoundMenu, MenuAnimationType
from datetime import datetime, timedelta, timezone

from Helpers.Config import cfg
from Helpers.downloadHelper import downloadJson
from Helpers.flyoutmsg import dlerr, dlsuc, dlwar
from Helpers.getValue import MINECRAFT_ICON, RELEASE, SNAPSHOT, setDownloadData, CACHE_PATH, getVersionsData, setVersionsData
from Helpers.outputHelper import logger
from Helpers.styleHelper import style_path
class ModsInterface(ScrollArea):
    def __init__(self, version, f, parent=None):
        super().__init__(parent=parent)
        self.Layout = QVBoxLayout(self)
        self.tool = CommandBar()
        self.tool.addAction(Action(FluentIcon.ADD, '添加'))
        self.tool.addSeparator()
        self.tool.addAction(Action(FluentIcon.ACCEPT, '启用'))
        self.tool.addAction(Action(FluentIcon.CLOSE, '禁用'))
        self.tool.addAction(Action(FluentIcon.DELETE, '删除'))
        self.Layout.addWidget(self.tool, alignment=Qt.AlignTop)
        self.table = TableWidget(self)
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        self.Layout.addWidget(self.table)
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.setWordWrap(False)
        self.table.setRowCount(3)
        self.table.setColumnCount(5)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.contextMenuEvent)

        self.setQss()
    def load(self):
        if os.path.exists(os.path.join(cfg.gamePath.value, "mods")):
            pass
    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def contextMenuEvent(self, pos):
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FluentIcon.ADD, '添加'))
        menu.addSeparator()
        menu.addActions([
            Action(FluentIcon.ACCEPT, '启用'),
            Action(FluentIcon.CLOSE, '禁用'),
            Action(FluentIcon.DELETE, '删除')
        ])

        menu.exec(self.table.mapToGlobal(pos), aniType=MenuAnimationType.DROP_DOWN)