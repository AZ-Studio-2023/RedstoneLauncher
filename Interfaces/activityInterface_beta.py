import os.path
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QLabel, QVBoxLayout
from qfluentwidgets import PlainTextEdit, ScrollArea, ExpandLayout, TitleLabel, SettingCardGroup, \
    ExpandGroupSettingCard, FluentIcon, PushButton, ProgressBar, TransparentToolButton, VBoxLayout, BodyLabel

from Helpers.styleHelper import style_path
import uuid


class ProgressComponent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.textLayout = QVBoxLayout(self)

        self.process = ProgressBar()
        self.process.setRange(0, 100)
        self.textLayout.addWidget(self.process)

        self.layout_1 = QHBoxLayout()
        self.state_button_1 = TransparentToolButton(FluentIcon.MORE)
        self.stateLabel_1 = BodyLabel(self.tr("获取必要数据"))
        self.layout_1.addWidget(self.state_button_1)
        self.layout_1.addWidget(self.stateLabel_1)
        self.textLayout.addLayout(self.layout_1)

        self.layout_2 = QHBoxLayout()
        self.state_button_2 = TransparentToolButton(FluentIcon.MORE)
        self.stateLabel_2 = BodyLabel(self.tr("补全游戏所需资源"))
        self.layout_2.addWidget(self.state_button_2)
        self.layout_2.addWidget(self.stateLabel_2)
        self.textLayout.addLayout(self.layout_2)

        self.layout_3 = QHBoxLayout()
        self.state_button_3 = TransparentToolButton(FluentIcon.MORE)
        self.stateLabel_3 = BodyLabel(self.tr("构建启动命令"))
        self.layout_3.addWidget(self.state_button_3)
        self.layout_3.addWidget(self.stateLabel_3)
        self.textLayout.addLayout(self.layout_3)

        self.layout_4 = QHBoxLayout()
        self.state_button_4 = TransparentToolButton(FluentIcon.MORE)
        self.stateLabel_4 = BodyLabel(self.tr("启动游戏进程"))
        self.layout_4.addWidget(self.state_button_4)
        self.layout_4.addWidget(self.stateLabel_4)
        self.textLayout.addLayout(self.layout_4)

        self.layout_5 = QHBoxLayout()
        self.state_button_5 = TransparentToolButton(FluentIcon.MORE)
        self.stateLabel_5 = BodyLabel(self.tr("游戏进程退出"))
        self.layout_5.addWidget(self.state_button_5)
        self.layout_5.addWidget(self.stateLabel_5)
        self.textLayout.addLayout(self.layout_5)

class activityInterface(ScrollArea):

    def __init__(self):
        super().__init__()
        self.setObjectName("activityInterface")
        self.expandLayout = ExpandLayout(self)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.activity = SettingCardGroup(self.tr("任务"), self)
        self.expandLayout.addWidget(self.activity)
        self.setQss()

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def addActivityCard(self, version="8", Card_uuid="5"):
        self.ActivityCard = ExpandGroupSettingCard(
            FluentIcon.APPLICATION,
            self.tr(f'{version}'),
            self.tr("游戏任务"),
            self.activity
        )
        self.ActivityCard.setObjectName("1")
        self.logger = PushButton(FluentIcon.QUICK_NOTE, self.tr("日志"))

        self.info = ProgressComponent()
        self.info.setObjectName(Card_uuid)

        self.ActivityCard.addWidget(self.logger)
        self.ActivityCard.addGroupWidget(self.info)
        self.activity.addSettingCard(self.ActivityCard)



