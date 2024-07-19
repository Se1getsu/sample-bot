#!/usr/bin/zsh

if [ -z "$1" ]; then
    info_webhook="default"
else
    info_webhook=$1
fi

if [ -z "$2" ]; then
    error_webhook="default"
else
    error_webhook=$2
fi

pip install -r ./requirements.txt -q
python3 main.py "$info_webhook" "$error_webhook"
