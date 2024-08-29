# coding:utf-8
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import *
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from Helpers.Config import cfg
from PyQt5.QtCore import Qt, QUrl

from Helpers.getValue import YEAR, AUTHOR, VERSION, FEEDBACK_URL, HELP_URL
from Helpers.styleHelper import style_path


class AboutSettingsInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.settingLabel = QLabel(self.tr("关于"), self)

        self.setObjectName("AboutSettingsInterface")
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
        self.aboutGroup = SettingCardGroup(self.tr('Redstone Launcher'), self.scrollWidget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            self.tr('打开帮助页面'),
            FIF.HELP,
            self.tr('帮助'),
            self.tr('从帮助页面上获取帮助与支持'),
            self.aboutGroup
        )
        self.feedbackCard = PushSettingCard(
            self.tr('提供反馈'),
            FIF.FEEDBACK,
            self.tr('提供反馈'),
            self.tr('通过提供反馈来帮助我们打造更好的应用'),
            self.aboutGroup
        )
        self.sponsor = ExpandGroupSettingCard(
            FIF.HEART,
            self.tr("赞助名单"),
            self.tr("给本项目赞助的热心人"),
            self.aboutGroup
        )

        self.aboutCard = PushSettingCard(
            self.tr('更新日志'),
            FIF.INFO,
            self.tr('关于'),
            '© ' + self.tr(' ') + f" {YEAR}, {AUTHOR}. " +
            self.tr('Version') + f" {VERSION}",
            self.aboutGroup
        )

        self.feedbackCard.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))

    def setSettingsQss(self):
        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/qss/{theme}.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
    def InitLayout(self):
        self.settingLabel.move(60, 63)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.sponsor)
        self.aboutGroup.addSettingCard(self.aboutCard)
        self.expandLayout.addWidget(self.aboutGroup)
    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

