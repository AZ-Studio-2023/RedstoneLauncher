import os.path
import time
from datetime import datetime

from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFontDatabase, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QScrollArea
from qfluentwidgets import PlainTextEdit, ScrollArea

from Helpers.flyoutmsg import dlsuc
from Helpers.getValue import getProcessData, getVersionsData, setVersionsData
from Helpers.styleHelper import style_path
from Helpers.downloadHelper import get_download_status

old_message = ""
finished_ver = []

class update_text(QThread):
    trigger = pyqtSignal()
    def __init__(self):
        super(update_text, self).__init__()

    def run(self):
        time.sleep(10)
        self.trigger.emit()

class downloadActivityInterface(QWidget):


    def __init__(self):
        super().__init__()
        self.setObjectName("loggerInterface")
        font_id = QFontDatabase.addApplicationFont(os.path.join("resource", "font", "Minecraft_UTF-8.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.mc_font = QFont(font_family)
        self.mc_font.setPointSize(12)
        self.setWindowTitle("下载任务")
        self.setWindowIcon(QIcon("resource/image/logo.png"))
        self.textEdit = PlainTextEdit()
        self.textEdit.setObjectName("logger")
        self.textEdit.ensureCursorVisible()
        self.textEdit.setFont(self.mc_font)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.textEdit, stretch=1)
        self.textEdit.setReadOnly(True)
        self.t = update_text()
        self.t.trigger.connect(self.t_func)
        self.t.start()
        self.textEdit.setStyleSheet('''
            LineEdit, TextEdit, PlainTextEdit {
                color: white;
                background-color: rgba(64,64,64,1);
                border: 1px solid rgba(0, 0, 0, 13);
                border-bottom: 1px solid rgba(0, 0, 0, 100);
                border-radius: 5px;
                /* font: 14px "Segoe UI", "Microsoft YaHei"; */
                padding: 0px 10px;
                selection-background-color: #00a7b3;
            }
    
            TextEdit,
            PlainTextEdit {
                padding: 2px 3px 2px 8px;
            }
    
            LineEdit:hover, TextEdit:hover, PlainTextEdit:hover {
                border: 1px solid rgba(0, 0, 0, 13);
                border-bottom: 1px solid rgba(0, 0, 0, 100);
            }
    
            LineEdit:focus {
                border-bottom: 1px solid rgba(0, 0, 0, 13);
                background-color: white;
            }
    
            TextEdit:focus,
            PlainTextEdit:focus {
                border-bottom: 1px solid #009faa;
                /* background-color: white; */
            }
    
            LineEdit:disabled, TextEdit:disabled,
            PlainTextEdit:disabled {
                color: rgba(0, 0, 0, 150);
                background-color: rgba(249, 249, 249, 0.3);
                border: 1px solid rgba(0, 0, 0, 13);
                border-bottom: 1px solid rgba(0, 0, 0, 13);
            }
    
            #lineEditButton {
                background-color: transparent;
                border-radius: 4px;
                margin: 0;
            }
    
            #lineEditButton:hover {
                background-color: rgba(0, 0, 0, 9);
            }
    
            #lineEditButton:pressed {
                background-color: rgba(0, 0, 0, 6);
            }
            ''')

    def t_func(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.setLog)
        self.timer.start(3000)

    def setLog(self):
        global old_message, finished_ver
        m = get_download_status()
        if m != old_message:
            self.textEdit.setPlainText(m)
            old_message = m
            if m == "没有正在进行的下载任务。":
                d = getVersionsData()
                if d not in finished_ver and d["downloading"]:
                    d["downloading"] = False
                    finished_ver.append(d)
                    dlsuc(self, f"{d['name']}安装完成！")
                    setVersionsData(d)

