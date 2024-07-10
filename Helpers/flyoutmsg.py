from PyQt5.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition


def dlsuc(parent, content, title="", show_time=3000):
    # convenient class mothod
    InfoBar.success(
        title=title,
        content=content,
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=show_time,
        parent=parent)