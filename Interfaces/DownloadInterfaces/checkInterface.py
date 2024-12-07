from PyQt5.QtCore import Qt, QPoint, QSize, QUrl, QRect, QPropertyAnimation, QThreadPool, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect, QLabel

from qfluentwidgets import (CardWidget, setTheme, Theme, IconWidget, BodyLabel, CaptionLabel, PushButton,
                            TransparentToolButton, FluentIcon, RoundMenu, Action, ElevatedCardWidget,
                            ImageLabel, isDarkTheme, FlowLayout, MSFluentTitleBar, SimpleCardWidget,
                            HeaderCardWidget, InfoBarIcon, HyperlinkLabel, HorizontalFlipView,
                            PrimaryPushButton, TitleLabel, PillPushButton, setFont, SingleDirectionScrollArea,
                            VerticalSeparator, MSFluentWindow, NavigationItemPosition, ScrollArea,
                            TransparentPushButton, MessageBoxBase, SubtitleLabel, ComboBox, LineEdit, StrongBodyLabel)

from Helpers.getValue import MINECRAFT_ICON, getVersionsData, FABRIC_ICON, FORGE_ICON
from Helpers.styleHelper import style_path


class AppCard(CardWidget):
    """ App card """

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(18, 18)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")

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

class checkInterface(ScrollArea):

    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.setObjectName("checkInterface")
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.setQss()

        self.Minecraft = AppCard(QIcon(MINECRAFT_ICON), "Minecraft", getVersionsData()["minecraft"], self)
        self.Minecraft.setFixedHeight(70)
        self.Minecraft.setObjectName("Minecraft")
        self.vBoxLayout.addWidget(self.Minecraft, alignment=Qt.AlignTop)

        self.Forge = AppCard(QIcon(FORGE_ICON), "Forge", getVersionsData()["forge"], self)
        self.Forge.setFixedHeight(70)
        self.Forge.setObjectName("Forge")
        self.vBoxLayout.addWidget(self.Forge, alignment=Qt.AlignTop)

        self.Fabric = AppCard(QIcon(FABRIC_ICON), "Fabric", getVersionsData()["fabric"], self)
        self.Fabric.setFixedHeight(70)
        self.Fabric.setObjectName("Fabric")
        self.vBoxLayout.addWidget(self.Fabric, alignment=Qt.AlignTop)

        self.Layout = FlowLayout()
        self.nameInput = LineEdit()
        self.nameInput.setPlaceholderText("请输入版本名")
        self.nameInput.setFixedWidth(150)
        if getVersionsData()["forge"] != "未选择":
            self.nameInput.setText(f"{getVersionsData()['minecraft']}-Forge {getVersionsData()['forge']}")
        elif getVersionsData()["fabric"] != "未选择":
            self.nameInput.setText(f"{getVersionsData()['minecraft']}-Fabric {getVersionsData()['fabric']}")
        else:
            self.nameInput.setText(getVersionsData()['minecraft'])
        self.submit = PrimaryPushButton(FluentIcon.DOWNLOAD, self.tr("开始下载"))
        self.submit.setContentsMargins(0, 25, 0, 0)
        self.Layout.setAlignment(Qt.AlignRight)
        self.Layout.addWidget(self.nameInput)
        self.Layout.addWidget(self.submit)
        self.vBoxLayout.addLayout(self.Layout)

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())



