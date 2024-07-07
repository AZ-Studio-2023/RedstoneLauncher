# coding:utf-8
from PyQt5.QtWidgets import *
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from Helpers.Config import cfg
from PyQt5.QtCore import Qt

class AppilacationSettingsInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.settingLabel = QLabel(self.tr("Settings"), self)

        self.setObjectName("AppilacationSettingsInterface")
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/qss/{theme}.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

        self.InitCards()
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)


        self.InitLayout()

    def InitCards(self):
        self.AppearanceGroup = SettingCardGroup(self.tr("Appearance"), self.scrollWidget)
        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr('Language'),
            self.tr('Set your preferred language for UI'),
            texts=['简体中文', '繁體中文', 'English', self.tr('Use system setting')],
            parent=self.AppearanceGroup
        )


    def InitLayout(self):
        self.settingLabel.move(60, 63)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.AppearanceGroup.addSettingCard(self.languageCard)
        self.expandLayout.addWidget(self.AppearanceGroup)
