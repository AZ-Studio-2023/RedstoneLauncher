# coding:utf-8
from enum import Enum

from Helpers.getValue import DEFAULT_GAME_PATH
from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtGui import QGuiApplication, QFont, QColor
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            ColorConfigItem, OptionsValidator, RangeConfigItem, RangeValidator, ColorValidator,
                            FolderListValidator, EnumSerializer, FolderValidator, ConfigSerializer, __version__, Theme)


class SongQuality(Enum):
    """ Online song quality enumeration class """

    STANDARD = "Standard quality"
    HIGH = "High quality"
    SUPER = "Super quality"
    LOSSLESS = "Lossless quality"


class MvQuality(Enum):
    """ MV quality enumeration class """

    FULL_HD = "Full HD"
    HD = "HD"
    SD = "SD"
    LD = "LD"


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class Config(QConfig):
    """ Config of application """

    gamePath = OptionsConfigItem(
        "gameFileGroup", "gamePath", DEFAULT_GAME_PATH, FolderValidator()
    )

    javaPath = OptionsConfigItem(
        "javaGroup", "javaPath", ""
    )

    language = OptionsConfigItem(
        "personalizeGroup", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer())

    themeMode = OptionsConfigItem(
        "personalizeGroup", "ThemeMode", Theme.LIGHT, OptionsValidator(Theme), EnumSerializer(Theme))

    source = OptionsConfigItem(
        "downloadGroup", "downloadSource", "BMCL API", OptionsValidator(["官方", "BMCL API"])
    )
    downloadMethod = OptionsConfigItem(
               "downloadGroup", "downloadMethod", "Aria2", OptionsValidator(["Aria2"])
    )

cfg = Config()
qconfig.load('config/config.json', cfg)
