# coding:utf-8
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import *
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from Helpers.Config import cfg
from PyQt5.QtCore import Qt, QUrl

from Helpers.getValue import YEAR, AUTHOR, VERSION, FEEDBACK_URL, HELP_URL, RELEASE_URL, AZ_URL, versionDetail
from Helpers.styleHelper import style_path


def changelog(parent):
    view = FlyoutView(
        title=f'Redstone Launcher {VERSION}更新日志 ',
        content=versionDetail,
        # image='resource/splash.png',
        isClosable=True
    )

    # add button to view
    button1 = PushButton(FIF.GITHUB, 'GitHub')
    button1.setFixedWidth(120)
    button1.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(RELEASE_URL)))
    view.addWidget(button1, align=Qt.AlignRight)

    button2 = PushButton('AZ Studio')
    button2.setFixedWidth(120)
    button2.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(AZ_URL)))
    view.addWidget(button2, align=Qt.AlignRight)

    view.widgetLayout.insertSpacing(1, 5)
    view.widgetLayout.addSpacing(5)

    # show view
    w = Flyout.make(view, parent.aboutCard, parent)
    view.closed.connect(w.close)


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
        self.aboutCard.clicked.connect(lambda: changelog(self))
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

