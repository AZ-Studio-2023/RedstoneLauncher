# coding:utf-8
from PyQt5.QtWidgets import QWidget

from qfluentwidgets import SwitchButton


class VersionListInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("VersionListInterface")
        self.switchButton = SwitchButton(parent=self)
        self.switchButton.move(48, 24)
        self.switchButton.checkedChanged.connect(self.onCheckedChanged)

    def onCheckedChanged(self, isChecked: bool):
        text = 'On' if isChecked else 'Off'
        self.switchButton.setText(text)