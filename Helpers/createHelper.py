import os
from Helpers.Config import cfg
import json
from Helpers.getValue import DATA_PATH, ACCOUNTS_PATH, COMMAND_PATH, LOG_PATH, CACHE_PATH, allPath

def check_and_create():
    if not os.path.exists(allPath):
        os.mkdir(allPath)
    if not os.path.exists(cfg.gamePath.value):
        os.mkdir(cfg.gamePath.value)
    if not os.path.exists(os.path.join(cfg.gamePath.value, "versions")):
        os.mkdir(os.path.join(cfg.gamePath.value, "versions"))
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)
    if not os.path.exists(ACCOUNTS_PATH):
        u = open(ACCOUNTS_PATH, "w")
        u.write(json.dumps({"accounts": []}))
        u.close()
    if not os.path.exists(COMMAND_PATH):
        os.mkdir(COMMAND_PATH)
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)
