from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QHBoxLayout, QVBoxLayout
from qfluentwidgets import FluentIcon, ExpandGroupSettingCard, SubtitleLabel, PrimaryPushButton, PushButton, ScrollArea, \
    ExpandLayout, SettingCardGroup, isDarkTheme, IconWidget, CardWidget, CaptionLabel, BodyLabel, TransparentToolButton, \
    IndeterminateProgressBar, OptionsSettingCard

from Helpers.getValue import MINECRAFT_ICON
from Helpers.styleHelper import style_path


class DownloadInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("DownloadInterface")
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
        self.expandLayout.addWidget(self.downloadGroup)
        self.downloadGroup.addSettingCard(self.vanilla)
        self.setQss()
    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())
