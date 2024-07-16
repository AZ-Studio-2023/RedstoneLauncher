import json
import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QPoint, QSize, QUrl, QRect, QPropertyAnimation, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect, QLabel

from qfluentwidgets import (CardWidget, setTheme, Theme, IconWidget, BodyLabel, CaptionLabel, PushButton,
                            TransparentToolButton, FluentIcon, RoundMenu, Action, ElevatedCardWidget,
                            ImageLabel, isDarkTheme, FlowLayout, MSFluentTitleBar, SimpleCardWidget,
                            HeaderCardWidget, InfoBarIcon, HyperlinkLabel, HorizontalFlipView,
                            PrimaryPushButton, TitleLabel, PillPushButton, setFont, SingleDirectionScrollArea,
                            VerticalSeparator, MSFluentWindow, NavigationItemPosition, ScrollArea,
                            TransparentPushButton, MessageBoxBase, SubtitleLabel, ComboBox, LineEdit)

from Helpers.getValue import MICROSOFT_ACCOUNT, LEGACY_ACCOUNT, THIRD_PARTY_ACCOUNT
from Helpers.flyoutmsg import dlsuc, dlwar
from Helpers.styleHelper import style_path

class AppCard(CardWidget):
    """ App card """

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.logger = PushButton(FluentIcon.QUICK_NOTE, self.tr("日志"))

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.logger.setFixedWidth(120)

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
        self.hBoxLayout.addWidget(self.logger, 0, Qt.AlignRight)

class activityInterface(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("activityInterface")
        self.title = TitleLabel()
        self.title.setText(self.tr("任务"))
        self.title.setContentsMargins(0, 0, 0, 10)
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.addWidget(self.title, alignment=Qt.AlignLeft)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(30, 60, 30, 30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.setQss()


    def addCard(self, icon, title, content, uuid):
        card = AppCard(icon, title, content, self)
        card.setObjectName(title)
        self.vBoxLayout.addWidget(card, alignment=Qt.AlignTop)

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def addActivityCard(self, version="1", Card_uuid="9"):
        self.addCard(FluentIcon.APPLICATION, version, "当前状态：", Card_uuid)




