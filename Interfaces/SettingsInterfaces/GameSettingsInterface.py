# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog
from qfluentwidgets import FluentIcon, ExpandGroupSettingCard, SubtitleLabel, PrimaryPushButton, PushButton, ScrollArea, \
    ExpandLayout, SettingCardGroup, isDarkTheme
from Helpers.Config import DEFAULT_GAME_PATH
from Helpers.Config import cfg


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
            FluentIcon.FOLDER,
            self.tr('首选Java运行时'),
            self.tr("选择运行游戏的首选Java运行时"),
            self.javaGroup
        )
    def InitLayout(self):
        self.settingLabel.move(60, 63)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.gameFileGroup.addSettingCard(self.gamePathCard)
        self.expandLayout.addWidget(self.gameFileGroup)
        
        self.gamePathCard.addGroupWidget(self.LabelFolder)
        self.gamePathCard.addGroupWidget(self.LabelAuto)
        self.gamePathCard.addWidget(self.changeFolder)
        self.gamePathCard.addWidget(self.AutoFolder)

    def setQss(self):
        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/qss/{theme}.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.gamePath) == folder:
            return
        cfg.set(cfg.gamePath, folder)
        self.LabelFolder.setText(self.tr(f"\n    当前目录为：{folder}\n"))

    def __FolederAutoCardClicked(self):
        cfg.set(cfg.gamePath, DEFAULT_GAME_PATH)
        self.LabelFolder.setText(self.tr(f"\n    当前目录为：{DEFAULT_GAME_PATH}\n"))
