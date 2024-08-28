# coding:utf-8
from PyQt5.QtWidgets import *
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from Helpers.Config import cfg
from PyQt5.QtCore import Qt

from Helpers.styleHelper import style_path


class AppilacationSettingsInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.settingLabel = QLabel(self.tr("应用程序设置"), self)

        self.setObjectName("AppilacationSettingsInterface")
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        self.InitCards()
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)


        self.InitLayout()
        self.setQss()

    def InitCards(self):
        self.personalizeGroup = SettingCardGroup(self.tr("个性化"), self.scrollWidget)
        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr('语言'),
            self.tr('设置用户界面的首选语言'),
            texts=['简体中文', '繁體中文', 'English', self.tr('使用系统设置')],
            parent=self.personalizeGroup
        )
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('深浅模式'),
            self.tr("更改应用程序的外观"),
            texts=[
                self.tr('浅色'), self.tr('深色'),
                self.tr('使用系统设置')
            ],
            parent=self.personalizeGroup
        )
        self.downloadGroup = SettingCardGroup(self.tr("下载设置"), self.scrollWidget)
        self.downloadSource = OptionsSettingCard(
            cfg.source,
            FIF.SEARCH_MIRROR,
            self.tr("下载源"),
            self.tr("下载游戏资源使用的源"),
            texts=["官方", "BMCL API"],
            parent=self.downloadGroup
        )
        self.downloadMethod = OptionsSettingCard(
            cfg.downloadMethod,
            FIF.CLOUD_DOWNLOAD,
            self.tr("下载方式"),
            self.tr("下载资源文件的方式，目前仅支持Aria2多线程下载"),
            texts=["Aria2"],
            parent=self.downloadGroup
        )
        self.betaGroup = SettingCardGroup(self.tr("实验性功能"), self.scrollWidget)
        self.debug = SwitchSettingCard(
            FIF.CODE,
            self.tr("Debug模式"),
            self.tr("关闭全局异常捕获，并输出更多调试信息。"),
            configItem=cfg.debug_card,
            parent=self.betaGroup
        )
        self.plugin = SwitchSettingCard(
            FIF.APPLICATION,
            self.tr("插件"),
            self.tr("开启插件功能，探索Redstone Launcher的更多玩法！"),
            cfg.PluginEnable,
            self.betaGroup
        )
        self.themeCard.optionChanged.connect(lambda ci: setTheme(cfg.get(ci)))


    def setSettingsQss(self):
        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/qss/{theme}.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
    def InitLayout(self):
        self.settingLabel.move(60, 63)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.personalizeGroup.addSettingCard(self.languageCard)
        self.personalizeGroup.addSettingCard(self.themeCard)
        self.downloadGroup.addSettingCard(self.downloadSource)
        self.downloadGroup.addSettingCard(self.downloadMethod)
        self.betaGroup.addSettingCard(self.debug)
        self.betaGroup.addSettingCard(self.plugin)
        self.expandLayout.addWidget(self.personalizeGroup)
        self.expandLayout.addWidget(self.downloadGroup)
        self.expandLayout.addWidget(self.betaGroup)

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

