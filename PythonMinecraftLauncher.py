# coding:utf-8
import sys
from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme, FluentTranslator
from Views.main import Window
from Helpers.Config import cfg

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # internationalization
    locale = cfg.get(cfg.language).value
    fluentTranslator = FluentTranslator(locale)
    settingTranslator = QTranslator()
    settingTranslator.load(locale, "MainWindow", ".", "resource/i18n")
    caonima = QTranslator()
    caonima.load("reaource/i18n/MainWindow.ts")

    setTheme(Theme.LIGHT)
    app = QApplication(sys.argv)
    app.installTranslator(fluentTranslator)
    app.installTranslator(settingTranslator)
    app.installTranslator(caonima)

    w = Window()
    w.show()
    app.exec_()
