#!/bin/bash

repository="https://github.com/NNTin/Reply-Dota-2-Reddit.git"
localFolder="/home/pi/Desktop/Reply-Dota-2-Reddit"
sensitive="/home/pi/Desktop/sensitive/Reply-Dota-2-Reddit"

rm -r -f "$localFolder"
git clone "$repository" "$localFolder"

cp "$sensitive/obot.py" "$localFolder/obot.py"
cp "$sensitive/steamapikey.py" "$localFolder/steamapi/steamapikey.py"

cd "$localFolder"

until python3 main.py; do
    echo "Respawning.." >&2
    sleep 1
done