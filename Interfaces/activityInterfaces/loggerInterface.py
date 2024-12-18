import os.path
import time
from datetime import datetime

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QFontDatabase, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QScrollArea
from qfluentwidgets import PlainTextEdit, ScrollArea

from Helpers.flyoutmsg import dlwar
from Helpers.getValue import getProcessData, LOG_PATH
from Helpers.styleHelper import style_path

old_log = {}
old_state = {}
T = False

class loggerInterface(QWidget):

    def __init__(self, process_uuid, version):
        super().__init__()
        self.setObjectName("loggerInterface")
        font_id = QFontDatabase.addApplicationFont(os.path.join("resource", "font", "Minecraft_UTF-8.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.mc_font = QFont(font_family)
        self.mc_font.setPointSize(12)
        self.uuid = process_uuid
        self.version = version
        self.setWindowTitle(f"游戏日志 | Version: {self.version} | Process_UUID: {self.uuid}")
        self.setWindowIcon(QIcon("resource/image/logo.png"))
        self.textEdit = PlainTextEdit()
        self.textEdit.setObjectName("logger")
        self.textEdit.ensureCursorVisible()
        self.textEdit.setFont(self.mc_font)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.textEdit, stretch=1)
        self.textEdit.setReadOnly(True)
        if self.uuid != "tip":
            for data in getProcessData():
                if data["uuid"] == self.uuid:
                    state = data["state"]
                    break
            self.textEdit.setPlainText(f"游戏日志 | Version: {self.version} | Process_UUID: {self.uuid}\n当前进程状态：{state}\n\n当前无游戏日志")
            old_log[self.uuid] = ""
            old_state[self.uuid] = ""
            self.timer = QTimer()
            self.timer.timeout.connect(self.setLog)
            self.timer.start(2)
        else:
            self.textEdit.setPlainText("您还没有启动游戏，这里没有可查看的任务")
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
    def setLog(self):
        global old_log, old_state, T
        path = os.path.join(LOG_PATH, self.uuid, "logs", "latest.log")
        if os.path.exists(path):
            u = open(path, "r", encoding="gbk")
            log = u.read()
            u.close()
            for data in getProcessData():
                if data["uuid"] == self.uuid:
                    state = data["state"]
                    if T and data["code"] == 5:
                        dlwar("刷新令牌失败！将使用旧的令牌启动", self, show_time=10000)
                        T = True
                    break
            if log != old_log[self.uuid]:
                old_log[self.uuid] = log
                self.textEdit.setPlainText(f"游戏日志 | Version: {self.version} | Process_UUID: {self.uuid}\n当前进程状态：{state}\n\n{log}")
            elif state != old_state[self.uuid]:
                old_state[self.uuid] = state
                self.textEdit.setPlainText(f"游戏日志 | Version: {self.version} | Process_UUID: {self.uuid}\n当前进程状态：{state}\n\n{log}")
        else:
            for data in getProcessData():
                if data["uuid"] == self.uuid:
                    state = data["state"]
                    break
            if state != old_state[self.uuid]:
                old_state[self.uuid] = state
                self.textEdit.setPlainText(f"游戏日志 | Version: {self.version} | Process_UUID: {self.uuid}\n当前进程状态：{state}\n\n当前无游戏日志")

