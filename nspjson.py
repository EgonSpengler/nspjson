#!/bin/python3

# Tinfoil-compatible json generator for serving NSP/NSZ
#
# By Tyler Adam // https://github.com/EgonSpengler/nspjson

import json
import os
import ntpath
import urllib.parse
import base64


def listfiles(dir):
    for root, folders, files in os.walk(dir):
        for file in folders + files:
            yield os.path.join(root, file)


# Where the files are accessible from your webserver
WEBROOT = "192.168.1.115/Media/Games/Consoles/Switch/NSP/"
PROTOCOL = "http://"
# Directory containing the files on disk
# (locally browseable directory, likely different from WEBROOT)
NSPDIR = "/base/Media/Games/Consoles/Switch/NSP/"
# Send switch.json to wherever you would like to serve it from
# (since "Media" is my browseable http directory, I will enter
#  192.168.1.115://Media/Switch/switch.json as my Tinfoil source)
OUTPUT_JSON = "/base/Media/Switch/switch.json"
MOTD = "Connected to Egon's Server!"

# Enable for HTTP Basic Auth in generated links
USE_AUTH = True
AUTH_USER = "guest"
AUTH_PASS = "iamuptonogood"

files = []
results = {}

auth_str = (PROTOCOL + AUTH_USER + ":" + AUTH_PASS + "@") if USE_AUTH else PROTOCOL

for filename in sorted(listfiles(NSPDIR)):
    if filename.lower().endswith(".nsp") or filename.lower().endswith(".nsz"):
        file = {}
        file["url"] = (urllib.parse.quote(auth_str + WEBROOT + ntpath.basename(filename), safe="/:@"))
        file["size"] = os.path.getsize(filename)
        print(" + added " + ntpath.basename(filename))
        files.append(file)

results["files"] = files
results["success"] = MOTD

with open(OUTPUT_JSON, "w") as fp:
    json.dump(results, fp=fp, sort_keys=True, indent=2)
    fp.close()

print("Wrote list to " + OUTPUT_JSON)
