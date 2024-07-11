import os
from Helpers.Config import cfg
import json

def check_and_create():
    if not os.path.exists(cfg.gamePath.value):
        os.mkdir(cfg.gamePath.value)
    if not os.path.exists(os.path.join(cfg.gamePath.value, "versions")):
        os.mkdir(os.path.join(cfg.gamePath.value, "versions"))
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists("data/accounts.json"):
        u = open("data/accounts.json", "w")
        u.write(json.dumps({"accounts": []}))
        u.close()
    if not os.path.exists("command"):
        os.mkdir("command")
