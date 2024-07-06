# coding:utf-8
import sys
from typing import Dict, Union

from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QApplication, QFrame, QWidget

from qfluentwidgets import (NavigationBar, NavigationItemPosition, NavigationWidget, MessageBox,FluentIconBase,
                            isDarkTheme, setTheme, Theme, setThemeColor, SearchLineEdit, NavigationBarPushButton,
                            PopUpAniStackedWidget, getFont, setFont)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, TitleBar
from typing import Dict, Union

from PyQt5.QtCore import Qt, pyqtSignal, QRect, QPropertyAnimation, QEasingCurve, pyqtProperty, QRectF
from PyQt5.QtGui import QFont, QPainter, QColor, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class ListViewHelper(NavigationBar):
    def insertItem(self, index: int, routeKey: str, icon: Union[str, QIcon, FluentIconBase], text: str, onClick=None,
                   selectable=True, selectedIcon=None, position=NavigationItemPosition.TOP):
        """ insert navigation tree item

        Parameters
        ----------
        index: int
            the insert position of parent widget

        routeKey: str
            the unique name of item

        icon: str | QIcon | FluentIconBase
            the icon of navigation item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        selectable: bool
            whether the item is selectable

        selectedIcon: str | QIcon | FluentIconBase
            the icon of navigation item in selected state

        position: NavigationItemPosition
            where the button is added
        """
        if routeKey in self.items:
            return

        w = NavigationBarPushButtonHelper(icon, text, selectable, selectedIcon, self)
        self.insertWidget(index, routeKey, w, onClick, position)
        return w

class NavigationBarPushButtonHelper(NavigationBarPushButton):
    """ Navigation bar push button """

    def __init__(self, icon: Union[str, QIcon, FIF], text: str, isSelectable: bool, selectedIcon=None, parent=None):
        super().__init__(icon, text, isSelectable, parent)
        self._selectedIcon = selectedIcon
        self._isSelectedTextVisible = True

        self.setFixedSize(180, 58)
        setFont(self, 11)