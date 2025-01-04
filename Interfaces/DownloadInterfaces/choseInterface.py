import json
import os.path

import requests
from PyQt5.QtCore import Qt, QThreadPool, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QHBoxLayout, QVBoxLayout, QAbstractItemView, QTableWidgetItem
from qfluentwidgets import FluentIcon, ExpandGroupSettingCard, SubtitleLabel, PrimaryPushButton, PushButton, ScrollArea, \
    VBoxLayout, SettingCardGroup, isDarkTheme, IconWidget, CardWidget, CaptionLabel, BodyLabel, TransparentToolButton, \
    IndeterminateProgressBar, OptionsSettingCard, ListWidget, TableWidget
from datetime import datetime, timedelta, timezone

from Helpers.Config import cfg
from Helpers.downloadHelper import downloadJson
from Helpers.flyoutmsg import dlerr, dlsuc, dlwar
from Helpers.getValue import MINECRAFT_ICON, RELEASE, SNAPSHOT, setDownloadData, CACHE_PATH, getVersionsData, setVersionsData
from Helpers.outputHelper import logger
from Helpers.styleHelper import style_path
from Interfaces.DownloadInterfaces.choseMod import choseMod
from Interfaces.DownloadInterfaces.checkInterface import checkInterface

url = ""

class getConfig(QThread):
    trigger = pyqtSignal(dict)
    def __init__(self):
        super(getConfig, self).__init__()

    def run(self):
        global url
        try:
            r = requests.get(url).json()
        except Exception as e:
            logger.error(f"错误：{e}")
            self.trigger.emit({"code": 502, "data":[]})
            return
        self.trigger.emit({"code": 200, "data":r})

class choseInterface(ScrollArea):
    def __init__(self, d_type, f, parent=None):
        global url
        super().__init__(parent=parent)
        self.p = parent
        self.d_type = d_type
        self.f = f
        self.setObjectName("choseInterface")
        self.VBoxLayout = QVBoxLayout(self)
        self.HBoxLayout = QHBoxLayout()
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.title = SubtitleLabel(self.tr("选择版本"), self)
        self.refresh = PushButton(FluentIcon.SYNC, self.tr("刷新"))
        self.refresh.setFixedSize(80, 35)
        if self.d_type == "Minecraft":
            self.refresh.clicked.connect(self.start)
        else:
            self.refresh.clicked.connect(self.mod_load)
        self.enter = PrimaryPushButton(FluentIcon.CHECKBOX, self.tr("确定"))
        self.enter.clicked.connect(self.enter_f)
        self.enter.setEnabled(False)
        self.enter.setFixedSize(78, 33)
        self.HBoxLayout.addWidget(self.title)
        self.HBoxLayout.setContentsMargins(10, 10, 10, 10)
        self.HBoxLayout.addWidget(self.refresh)
        self.HBoxLayout.addWidget(self.enter)
        self.HBoxLayout.setAlignment(Qt.AlignTop)
        self.VBoxLayout.addLayout(self.HBoxLayout)
        self.table = TableWidget()
        self.table.setBorderVisible(True)
        self.table.verticalHeader().hide()
        self.table.setWordWrap(False)
        self.table.setBorderRadius(8)
        self.table.setColumnCount(3)
        self.table.setRowCount(10)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        if self.d_type == "Minecraft":
            self.table.setHorizontalHeaderLabels([self.tr('版本号'), self.tr('类型'), self.tr('发布时间')])
        elif self.d_type == "Fabric":
            self.table.setHorizontalHeaderLabels([self.tr('版本号'), self.tr('Minecraft'), self.tr('稳定性')])
        else:
            self.table.setHorizontalHeaderLabels([self.tr('版本号'), self.tr('Minecraft'), self.tr('发布时间')])
        self.table.currentItemChanged.connect(self.changed_func)
        self.VBoxLayout.addWidget(self.table)
        self.setQss()

        self.pool = QThreadPool()
        self.start()
        self.gc = getConfig()
        self.gc.trigger.connect(self.load_versions)
        self.mod_load()

    def changed_func(self):
        if getVersionsData()["downloading"]:
            self.enter.setText("当前正在下载游戏，可前往任务页查看详情")
            self.enter.setEnabled(False)
        else:
            self.enter.clicked.connect(self.enter_f)
            self.enter.setEnabled(True)

    def setQss(self):
        with open(style_path(), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def mod_load(self):
        global url
        if self.d_type == "Forge":
            url = f"https://bmclapi2.bangbang93.com/forge/minecraft/{getVersionsData()['minecraft']}"
            self.gc.start()
        elif self.d_type == "Fabric":
            if cfg.source.value == "官方":
                 url = f"https://meta.fabricmc.net/v2/versions/loader/{getVersionsData()['minecraft']}"
            else:
                url = f"https://bmclapi2.bangbang93.com/fabric-meta/v2/versions/loader/{getVersionsData()['minecraft']}"
            self.gc.start()

    def start(self):
        if self.d_type == "Minecraft":
            self.download = downloadJson()
            self.download.signals.progress.connect(self.load_versions)
            if cfg.source.value == "官方":
                url = "http://launchermeta.mojang.com/mc/game/version_manifest.json"
            else:
                url = "https://bmclapi2.bangbang93.com/mc/game/version_manifest.json"
            setDownloadData({"url": url, "path": os.path.join(CACHE_PATH, "version_manifest.json")})
            self.pool.start(self.download)

    def enter_f(self):
        if self.d_type == "Minecraft":
            index = self.table.currentRow()
            version = self.table.item(index, 0).text()
            d = getVersionsData()
            d["minecraft"] = version
            setVersionsData(d)
            self.f(choseMod(self.f, self.p), "模组加载器")
        elif self.d_type == "Forge":
            index = self.table.currentRow()
            version = self.table.item(index, 0).text()
            d = getVersionsData()
            d["forge"] = version
            d["fabric"] = "未选择"
            self.f(checkInterface(self.p), "总览")
        elif self.d_type == "Fabric":
            index = self.table.currentRow()
            version = self.table.item(index, 0).text()
            d = getVersionsData()
            d["fabric"] = version
            d["forge"] = "未选择"
            self.f(checkInterface(self.p), "总览")



    def load_versions(self, r):
        if self.d_type == "Minecraft":
            if os.path.exists(os.path.join(CACHE_PATH, "version_manifest.json")):
                u = open(os.path.join(CACHE_PATH, "version_manifest.json"), "r", encoding='utf-8')
                data = json.loads(u.read())
                u.close()
                data = data["versions"]
                self.table.setRowCount(0)
                self.table.setRowCount(len(data))
                for num, j in enumerate(data):
                    utc_time_str = j["releaseTime"]
                    utc_time = datetime.fromisoformat(utc_time_str)
                    cn_timezone = timezone(timedelta(hours=8))
                    cn_time = str(utc_time.replace(tzinfo=timezone.utc).astimezone(cn_timezone))
                    self.table.setItem(num, 0, QTableWidgetItem(j["id"]))
                    self.table.setItem(num, 1, QTableWidgetItem(j["type"]))
                    self.table.setItem(num, 2, QTableWidgetItem(cn_time))
                self.table.resizeColumnsToContents()
                if r == "ok":
                    dlsuc(content="数据获取成功", parent=self.p)
                else:
                    dlwar(content="数据获取失败，已使用本地数据缓存", parent=self.p)
            else:
                dlerr("数据获取失败", parent=self.p)
        elif self.d_type == "Forge":
            try:
                if r["code"] == 200:
                    dlsuc(content="数据获取成功", parent=self.p)
                    data = r["data"]
                    if len(data) == 0:
                        dlwar("无可用版本", parent=self.p)
                    self.table.setRowCount(0)
                    self.table.setRowCount(len(data))
                    for num, j in enumerate(data):
                        self.table.setItem(num, 0, QTableWidgetItem(j["version"]))
                        self.table.setItem(num, 1, QTableWidgetItem(j["mcversion"]))
                        self.table.setItem(num, 2, QTableWidgetItem(j["modified"]))
                    self.table.resizeColumnsToContents()
                else:
                    dlerr("数据获取失败", parent=self.p)
            except:
                dlwar("无可用版本", parent=self.p)
            self.gc.quit()
        elif self.d_type == "Fabric":
            try:
                if r["code"] == 200:
                    dlsuc(content="数据获取成功", parent=self.p)
                    data = r["data"]
                    if len(data) == 0:
                        dlwar("无可用版本", parent=self.p)
                    self.table.setRowCount(0)
                    self.table.setRowCount(len(data))
                    for num, j in enumerate(data):
                        if j["loader"]["stable"]:
                            s = "是"
                        else:
                            s = "否"
                        self.table.setItem(num, 0, QTableWidgetItem(j["loader"]["version"]))
                        self.table.setItem(num, 1, QTableWidgetItem(j["intermediary"]["version"]))
                        self.table.setItem(num, 2, QTableWidgetItem(s))
                    self.table.resizeColumnsToContents()
                else:
                    dlerr("数据获取失败", parent=self.p)
            except:
                dlwar("无可用版本", parent=self.p)
            self.gc.quit()

