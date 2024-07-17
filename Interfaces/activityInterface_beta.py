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
                            TransparentPushButton, MessageBoxBase, SubtitleLabel, ComboBox, LineEdit, ProgressBar)

from Helpers.getValue import MICROSOFT_ACCOUNT, LEGACY_ACCOUNT, THIRD_PARTY_ACCOUNT
from Helpers.flyoutmsg import dlsuc, dlwar
from Helpers.styleHelper import style_path
from Helpers.getValue import getProcessData

local_process = []
local_process_data = {}

class AppCard(CardWidget):
    """ App card """

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.iconWidget.setFixedSize(18, 18)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.process = ProgressBar(self)
        self.process.setRange(0, 100)
        self.stopping = PushButton(FluentIcon.CLOSE, self.tr("强制停止"))
        self.logger = PushButton(FluentIcon.QUICK_NOTE, self.tr("日志"))

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.logger.setFixedWidth(120)
        self.stopping.setFixedWidth(120)

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
        self.hBoxLayout.addWidget(self.process, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.stopping, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.logger, 0, Qt.AlignRight)

    def change_state(self, state: str):
        self.contentLabel.setText(f"当前状态：{state}")

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
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_process)
        self.timer.start(1500)

    def change_process(self):
        global local_process
        global local_process_data
        data = getProcessData()
        for i in data:
            if i["uuid"] in local_process:
                card = local_process_data[i["uuid"]]
                card.change_state(i["state"])
            else:
                self.addActivityCard(i["version"], i["uuid"])
                local_process.append(i["uuid"])
                card = local_process_data[i["uuid"]]
                card.change_state(i["state"])

    def addCard(self, icon, title, content, cuuid):
        global local_process_data
        card = AppCard(icon, title, content, self)
        card.setObjectName(cuuid)
        local_process_data[cuuid] = card
        self.vBoxLayout.addWidget(card, alignment=Qt.AlignTop)

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def addActivityCard(self, version: str, Card_uuid: str):
        self.addCard(FluentIcon.APPLICATION, version, "当前状态：", Card_uuid)