from qfluentwidgets import Theme

from Helpers.Config import cfg


def style_path(theme=Theme.AUTO):
    theme = cfg.theme if theme == Theme.AUTO else theme
    return f"resource/qss/{theme.value.lower()}.qss"
