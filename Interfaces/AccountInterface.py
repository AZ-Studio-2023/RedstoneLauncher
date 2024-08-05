import json
import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QPoint, QSize, QUrl, QRect, QPropertyAnimation
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


class Add_Account_MessageBox(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('添加游戏账号')
        self.type_Label = QLabel("账号类型:", self)
        self.type_Label.setStyleSheet("QLabel{font-size:15px;font-weight:normal;font-family:Microsoft YaHei;}")
        self.type_Box = ComboBox()
        self.type_Box.addItems(["离线登录"])
        self.name_Label = QLabel("玩家名:", self)
        self.name_Label.setStyleSheet("QLabel{font-size:15px;font-weight:normal;font-family:Microsoft YaHei;}")
        self.username = LineEdit()
        self.username.setPlaceholderText('输入离线玩家名')
        self.username.setClearButtonEnabled(True)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.type_Label)
        self.viewLayout.addWidget(self.type_Box)
        self.viewLayout.addWidget(self.name_Label)
        self.viewLayout.addWidget(self.username)

        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(350)


class AppCard(CardWidget):
    """ App card """

    def __init__(self, icon, title, content, dic, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.delButton = TransparentToolButton(FluentIcon.DELETE, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(18, 18)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.delButton.setFixedWidth(120)

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
        self.hBoxLayout.addWidget(self.delButton, 0, Qt.AlignRight)
        self.delButton.clicked.connect(lambda: self.del_account(dic=dic))

    def del_account(self, dic):
        f = open("data/accounts.json", "r")
        data = json.loads(f.read())["accounts"]
        f.close()
        try:
            data.remove(dic)
        except ValueError:
            return 0
        f = open("data/accounts.json", "w")
        f.write(json.dumps({"accounts": data}))
        f.close()
        self.setVisible(False)


class AccountInterface(ScrollArea):

    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.setObjectName("AccountInterface")
        self.title = TitleLabel()
        self.title.setText(self.tr("游戏账号"))
        self.title.setContentsMargins(0, 0, 0, 10)
        self.hBoxLayout = QHBoxLayout()
        self.addButton = TransparentPushButton(FluentIcon.ADD_TO, self.tr("添加"))
        self.addButton.clicked.connect(self.showMessage)
        self.hBoxLayout.addWidget(self.title, alignment=Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.addButton, alignment=Qt.AlignRight | Qt.AlignTop)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(30, 60, 30, 30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.load_account()
        self.setQss()

    def addCard(self, icon, title, content, dic):
        card = AppCard(icon, title, content, dic, self)
        card.setFixedHeight(70)
        card.setObjectName(title)
        self.vBoxLayout.addWidget(card, alignment=Qt.AlignTop)

    def load_account(self):
        f = open("data/accounts.json", "r")
        data = json.loads(f.read())["accounts"]
        f.close()
        for account in data:
            if account["type"] == "Microsoft":
                self.addCard(QIcon(MICROSOFT_ACCOUNT), account["name"], "微软登录", account)
            elif account["type"] == "Legacy":
                self.addCard(QIcon(LEGACY_ACCOUNT), account["name"], "离线登录", account)
            else:
                self.addCard(QIcon(THIRD_PARTY_ACCOUNT), account["name"], "第三方登录", account)
    def add_account(self, account_type, name):
        f = open("data/accounts.json", "r")
        data = json.loads(f.read())["accounts"]
        f.close()
        if account_type == "Legacy":
            data.append({"name": name, "type": "Legacy"})
            self.addCard(QIcon(LEGACY_ACCOUNT), name, "离线登录", {"name": name, "type": "Legacy"})
        elif account_type == "Microsoft":
            pass  # 由于还在申请API 所以微软登录需要等审核通过后完善
        else:
            pass  # 第三方登录逻辑
        f = open("data/accounts.json", "w")
        f.write(json.dumps({"accounts": data}))
        f.close()
    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def showMessage(self):
        w = Add_Account_MessageBox(self.window())
        if w.exec():
            if w.username.text() != "":
                if w.type_Box.text() == "离线登录":
                    self.add_account(name=w.username.text(), account_type="Legacy")
                else:
                    pass
