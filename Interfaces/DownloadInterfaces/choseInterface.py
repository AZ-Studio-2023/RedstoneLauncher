import json
import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QHBoxLayout, QVBoxLayout
from qfluentwidgets import FluentIcon, ExpandGroupSettingCard, SubtitleLabel, PrimaryPushButton, PushButton, ScrollArea, \
    ExpandLayout, SettingCardGroup, isDarkTheme, IconWidget, CardWidget, CaptionLabel, BodyLabel, TransparentToolButton, \
    IndeterminateProgressBar, OptionsSettingCard
from datetime import datetime, timedelta, timezone

from Helpers.getValue import MINECRAFT_ICON, RELEASE, SNAPSHOT
from Helpers.styleHelper import style_path

added_list = []


class AppCard(CardWidget):
    """ App card """

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.iconWidget.setFixedSize(18, 18)
        self.title = title
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.download = PushButton(FluentIcon.DOWNLOAD, self.tr("下载"))

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.download.setFixedWidth(120)

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
        self.hBoxLayout.addWidget(self.download, 0, Qt.AlignRight)


class choseInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("choseInterface")
        self.expandLayout = ExpandLayout(self)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.downloadGroup = SettingCardGroup(self.tr("游戏下载"), self)
        self.vanilla = ExpandGroupSettingCard(
            QIcon(MINECRAFT_ICON),
            self.tr("Minecraft"),
            self.tr("要安装的Minecraft版本"),
            self.downloadGroup
        )
        self.refresh = PushButton(FluentIcon.SYNC, self.tr("刷新"))
        self.refresh.clicked.connect(self.load_versions)
        self.vanilla.addWidget(self.refresh)
        self.expandLayout.addWidget(self.downloadGroup)
        self.downloadGroup.addSettingCard(self.vanilla)
        self.setQss()
        self.load_versions()

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def load_versions(self):
        global added_list
        if os.path.exists(os.path.join("cache", "version_manifest.json")) and len(added_list) == 0:
            u = open(os.path.join("cache", "version_manifest.json"), "r", encoding='utf-8')
            data = json.loads(u.read())
            u.close()
            data = data["versions"]
            for j in data:
                utc_time_str = j["releaseTime"]
                utc_time = datetime.fromisoformat(utc_time_str)
                cn_timezone = timezone(timedelta(hours=8))
                cn_time = utc_time.replace(tzinfo=timezone.utc).astimezone(cn_timezone)
                if j["type"] == "snapshot":
                    self.addCard(QIcon(SNAPSHOT), j["id"], cn_time.strftime("%Y/%m/%d %H:%M:%S"))
                else:
                    self.addCard(QIcon(RELEASE), j["id"], cn_time.strftime("%Y/%m/%d %H:%M:%S"))
                added_list.append(j["id"])

    def addCard(self, icon, title, content):
        card = AppCard(icon, title, content, self)
        card.setFixedHeight(70)
        card.setObjectName(title)
        self.vanilla.addGroupWidget(card)
