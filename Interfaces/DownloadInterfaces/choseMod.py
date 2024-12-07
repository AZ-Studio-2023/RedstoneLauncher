import json
import os.path
import sys
import uuid
from pathlib import Path
import pyperclip
from PyQt5.QtCore import Qt, QPoint, QSize, QUrl, QRect, QPropertyAnimation, QThreadPool
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect, QLabel

from qfluentwidgets import (CardWidget, setTheme, Theme, IconWidget, BodyLabel, CaptionLabel, PushButton,
                            TransparentToolButton, FluentIcon, RoundMenu, Action, ElevatedCardWidget,
                            ImageLabel, isDarkTheme, FlowLayout, MSFluentTitleBar, SimpleCardWidget,
                            HeaderCardWidget, InfoBarIcon, HyperlinkLabel, HorizontalFlipView,
                            PrimaryPushButton, TitleLabel, PillPushButton, setFont, SingleDirectionScrollArea,
                            VerticalSeparator, MSFluentWindow, NavigationItemPosition, ScrollArea,
                            TransparentPushButton, MessageBoxBase, SubtitleLabel, ComboBox, LineEdit, StrongBodyLabel)

from Helpers.authHelper import MicrosoftLogin, get_offline_player_uuid
from Helpers.getValue import MICROSOFT_ACCOUNT, LEGACY_ACCOUNT, THIRD_PARTY_ACCOUNT, ACCOUNTS_PATH, CACHE_PATH
from Helpers.flyoutmsg import dlsuc, dlwar
from Helpers.getValue import MINECRAFT_ICON, FORGE_ICON, FABRIC_ICON
from Helpers.styleHelper import style_path
from Interfaces.DownloadInterfaces.checkInterface import checkInterface


class AppCard(CardWidget):
    """ App card """

    def __init__(self, icon, title, content, f, parent=None):
        super().__init__(parent)
        self.f = f
        self.p = parent
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.choseButton = TransparentToolButton(FluentIcon.RIGHT_ARROW, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(28, 28)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.choseButton.setFixedWidth(45)
        self.choseButton.clicked.connect(self.next)

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
        self.hBoxLayout.addWidget(self.choseButton, 0, Qt.AlignRight)
    def next(self):
        from Interfaces.DownloadInterfaces.choseInterface import choseInterface
        if self.titleLabel.text() == "Forge":
            self.f(choseInterface("Forge", self.f, self.p), "Forge")
        elif self.titleLabel.text() == "Fabric":
            self.f(choseInterface("Fabric", self.f, self.p), "Fabric")
        else:
            self.f(checkInterface(), "总览")




class choseMod(ScrollArea):

    def __init__(self, f, parent=None):
        super().__init__()
        self.setObjectName("choseModInterface")
        self.f = f
        self.p = parent
        self.title = TitleLabel()
        self.title.setText(self.tr("选择模组加载器"))
        self.title.setContentsMargins(0, 0, 0, 10)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.addCard(QIcon(MINECRAFT_ICON),"跳过", "不安装模组加载器，享受原版之乐")
        self.addCard(QIcon(FORGE_ICON),"Forge", "安装Forge模组加载器")
        self.addCard(QIcon(FABRIC_ICON),"Fabric", "安装Fabric模组加载器")


        self.setQss()

    def addCard(self, icon, title, content):
        card = AppCard(icon, title, content, self.f, parent=self.p)
        card.setFixedHeight(70)
        card.setObjectName(title)
        self.vBoxLayout.addWidget(card, alignment=Qt.AlignTop)

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

