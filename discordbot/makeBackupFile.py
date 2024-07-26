import os
import shelve

backup = os.path.join(os.path.dirname(__file__), "backup")

with shelve.open(backup, "c") as db:
    if "guilds" not in db:
        db["guilds"] = {}
    if "users" not in db:
        db["users"] = {}
