import os.path

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QScrollArea
from qfluentwidgets import PlainTextEdit, ScrollArea

from Helpers.styleHelper import style_path
from Helpers.getValue import getStatus

old_log = ""

class loggerInterface(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("loggerInterface")
        self.textEdit = PlainTextEdit()
        self.textEdit.setObjectName("logger")
        self.textEdit.ensureCursorVisible()
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.textEdit, stretch=1)
        self.textEdit.setReadOnly(True)
        self.textEdit.setPlainText("当前无游戏日志")
        self.timer = QTimer()
        self.timer.timeout.connect(self.setLog)
        self.timer.start(1500)
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
        global old_log
        if getStatus():
            if os.path.exists("logs/latest.log"):
                u = open("logs/latest.log", "r", encoding="gbk")
                log = u.read()
                u.close()
                if log != old_log:
                    old_log = log
                    self.textEdit.setPlainText(log)

