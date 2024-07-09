import os
from Helpers.Config import cfg


def check_and_create():
    if not os.path.exists(cfg.gamePath.value):
        os.mkdir(cfg.gamePath.value)
    if not os.path.exists(os.path.join(cfg.gamePath.value, "versions")):
        os.mkdir(os.path.join(cfg.gamePath.value, "versions"))
