# coding:utf-8
import random

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QHBoxLayout, QVBoxLayout
from qfluentwidgets import FluentIcon, ExpandGroupSettingCard, SubtitleLabel, PrimaryPushButton, PushButton, ScrollArea, \
    ExpandLayout, SettingCardGroup, isDarkTheme, IconWidget, CardWidget, CaptionLabel, BodyLabel, TransparentToolButton, \
    IndeterminateProgressBar, OptionsSettingCard

import Helpers.javaHelper
from Helpers.Config import DEFAULT_GAME_PATH
from Helpers.Config import cfg
from Helpers.flyoutmsg import dlsuc
from Helpers.getValue import JAVA_RUNTIME
from Helpers.javaHelper import GetJava_Local, GetJava_Global
from Helpers.styleHelper import style_path

java_list_path = []


class AppCard(CardWidget):
    """ App card """

    def __init__(self, icon, title, content, dic, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.acceptButton = TransparentToolButton(FluentIcon.ACCEPT_MEDIUM, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.acceptButton.setFixedWidth(120)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.acceptButton, 0, Qt.AlignRight)

        self.acceptButton.clicked.connect(self.set_path)

    def set_path(self):
        if not cfg.javaPath.value == self.contentLabel.text():
            cfg.set(cfg.javaPath, self.contentLabel.text())
            self.titleLabel.setText(self.titleLabel.text() + "（当前）")


class GameSettingsInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("GameSettingsInterface")
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel = QLabel(self.tr("游戏设置"), self)
        self.settingLabel.setObjectName('settingLabel')

        self.InitCards()
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.InitLayout()
        self.setQss()

    def InitCards(self):
        self.gameFileGroup = SettingCardGroup(self.tr("游戏文件"), self.scrollWidget)
        self.gamePathCard = ExpandGroupSettingCard(
            FluentIcon.FOLDER,
            self.tr('修改存储目录'),
            self.tr("修改游戏文件存储目录"),
            self.gameFileGroup
        )
        self.LabelFolder = SubtitleLabel(self.tr(f"\n    当前目录为：{cfg.gamePath.value}\n"), self)
        self.LabelAuto = SubtitleLabel(self.tr(f"\n    默认目录为：{DEFAULT_GAME_PATH}\n"), self)
        self.changeFolder = PrimaryPushButton(self.tr("选择目录"), self)
        self.changeFolder.clicked.connect(self.__onDownloadFolderCardClicked)
        self.AutoFolder = PushButton(self.tr("恢复默认"), self)
        self.AutoFolder.clicked.connect(self.__FolederAutoCardClicked)
        self.javaGroup = SettingCardGroup(self.tr("Java运行时"), self.scrollWidget)
        self.javaCard = ExpandGroupSettingCard(
            FluentIcon.APPLICATION,
            self.tr('首选Java运行时'),
            self.tr("选择运行游戏的首选Java运行时"),
            self.javaGroup
        )
        self.autoFindGlobal = PushButton("全局查找")
        self.autoFindLocal = PrimaryPushButton("快速查找")

        self.bar = IndeterminateProgressBar(self)
        self.bar.setVisible(False)

        self.autoFindLocal.clicked.connect(self.start_local_find)
        self.autoFindGlobal.clicked.connect(self.start_global_find)
        
        self.loaclFindWorker = GetJava_Local()
        self.globalFindWorker = GetJava_Global()

        self.loaclFindWorker.finished.connect(self.local_finished)
        self.globalFindWorker.finished.connect(self.global_finished)

        self.loaclFindWorker.start()

    def start_local_find(self):
        self.bar.setVisible(True)
        self.autoFindLocal.setEnabled(False)
        self.loaclFindWorker.start()

    def start_global_find(self):
        self.bar.setVisible(True)
        self.autoFindGlobal.setEnabled(False)
        self.globalFindWorker.start()

    def local_finished(self, data):
        self.bar.setVisible(False)
        self.autoFindLocal.setEnabled(True)
        self.loaclFindWorker.quit()
        if cfg.javaPath.value == "":
            if len(data) >= 1:
                cfg.set(cfg.javaPath.value, data[0].path)
        for java in data:
            self.addCard(QIcon(JAVA_RUNTIME), java.version, java.path)
        dlsuc(self, f"共计找到了 {len(data)} 个Java运行时", "快速查找完成", 6000)

    def global_finished(self, data):
        self.bar.setVisible(False)
        self.autoFindGlobal.setEnabled(True)
        self.globalFindWorker.quit()
        if cfg.javaPath.value == "":
            if len(data) >= 1:
                cfg.set(cfg.javaPath, data[0].path)
        for java in data:
            self.addCard(QIcon(JAVA_RUNTIME), java.version, java.path)

        dlsuc(self, f"共计找到了 {len(data)} 个Java运行时", "全局查找完成", 6000)

    def InitLayout(self):
        self.settingLabel.move(60, 63)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.gameFileGroup.addSettingCard(self.gamePathCard)
        self.expandLayout.addWidget(self.gameFileGroup)
        self.expandLayout.addWidget(self.javaGroup)
        self.javaGroup.addSettingCard(self.javaCard)
        self.gamePathCard.addGroupWidget(self.LabelFolder)
        self.gamePathCard.addGroupWidget(self.LabelAuto)
        self.gamePathCard.addWidget(self.changeFolder)
        self.gamePathCard.addWidget(self.AutoFolder)
        self.javaCard.addWidget(self.bar)
        self.javaCard.addWidget(self.autoFindGlobal)
        self.javaCard.addWidget(self.autoFindLocal)

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("选择文件夹"), "./")
        if not folder or cfg.get(cfg.gamePath) == folder:
            return
        cfg.set(cfg.gamePath, folder)
        self.LabelFolder.setText(self.tr(f"\n    当前目录为：{folder}\n"))

    def __FolederAutoCardClicked(self):
        cfg.set(cfg.gamePath, DEFAULT_GAME_PATH)
        self.LabelFolder.setText(self.tr(f"\n    当前目录为：{DEFAULT_GAME_PATH}\n"))

    def addCard(self, icon, title, content):
        global java_list_path
        for item in java_list_path:
            java_card = self.findChild(AppCard, item)
            java_card.deleteLater()
            java_list_path.remove(item)
        card = AppCard(icon, title, content, self)
        card.setFixedHeight(70)
        card.setObjectName(content)
        if cfg.javaPath.value == card.contentLabel.text():
            card.titleLabel.setText(card.titleLabel.text() + "（当前）")
        java_list_path.append(content)
        self.javaCard.addGroupWidget(card)
