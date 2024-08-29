# coding:utf-8
import sys
from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtWidgets import QApplication, QMessageBox
from qfluentwidgets import setTheme, Theme, FluentTranslator
from Views.main import Window
from Helpers.Config import cfg
from Helpers.createHelper import check_and_create

if not cfg.debug_card.value:
    def global_exception_handler(exc_type, exc_value, exc_traceback):
        msesg = '{}\n{}\n{}'.format(str(exc_type), str(exc_value), str(exc_traceback))
        QMessageBox.critical(w, "啊偶，出错了", msesg, QMessageBox.Yes)
    sys.excepthook = global_exception_handler

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # internationalization
    locale = cfg.get(cfg.language).value
    fluentTranslator = FluentTranslator(locale)
    settingTranslator = QTranslator()
    settingTranslator.load(locale, "MainWindow", ".", "resource/i18n")
    Translator = QTranslator()
    Translator.load("reaource/i18n/MainWindow.ts")

    check_and_create()

    setTheme(cfg.themeMode.value)

    app = QApplication(sys.argv)
    app.installTranslator(fluentTranslator)
    app.installTranslator(settingTranslator)
    app.installTranslator(caonima)

    w = Window()
    w.show()
    app.exec_()
