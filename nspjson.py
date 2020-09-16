#!/usr/bin/env python3

# Tinfoil-compatible json generator for serving NSP/NSZ
#
# By Tyler Adam // https://github.com/EgonSpengler/nspjson

import json
import os
import ntpath
import urllib.parse
import base64
from configparser import ConfigParser


def listfiles(dir):
    for root, folders, files in os.walk(dir):
        for file in folders + files:
            yield os.path.join(root, file)

#Read settings from config.ini
config_object = ConfigParser()
config_object.read("config.ini")
settings = config_object["SETTINGS"]

# Where the files are accessible from your webserver
WEBROOT = settings.get("webroot")
PROTOCOL = settings.get("protocol", "http://")
# Directory containing the files on disk
# (locally browseable directory, likely different from WEBROOT)
NSPDIR = settings.get("nspdir", ".")
# Send switch.json to wherever you would like to serve it from
# (since "Media" is my browseable http directory, I will enter
#  192.168.1.115://Media/Switch/switch.json as my Tinfoil source)
OUTPUT_JSON = os.path.join(settings.get("output", '.'), "switch.json")
MOTD = settings.get("motd")

# Enable for HTTP Basic Auth in generated links
USE_AUTH = settings.getboolean("use_auth", fallback=False)
AUTH_USER = settings.get("auth_user")
AUTH_PASS = settings.get("auth_pass")

files = []
results = {}

auth_str = (PROTOCOL + AUTH_USER + ":" + AUTH_PASS + "@") if USE_AUTH else PROTOCOL

for filename in sorted(listfiles(NSPDIR)):
    if filename.lower().endswith(".nsp") or filename.lower().endswith(".nsz"):
        file = {}
        file["url"] = (urllib.parse.quote(auth_str + WEBROOT + os.path.relpath(filename, NSPDIR), safe="/:@"))
        file["size"] = os.path.getsize(filename)
        print(" + added " + ntpath.basename(filename))
        files.append(file)

results["files"] = files
results["success"] = MOTD

with open(OUTPUT_JSON, "w") as fp:
    json.dump(results, fp=fp, sort_keys=True, indent=2)
    fp.close()

print("Wrote list to " + OUTPUT_JSON)
