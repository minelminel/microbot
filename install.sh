#!/usr/bin/env bash
# 
# RASPBERRY PI INSTALLATION SCRIPT
# 
# curl https://raw.githubusercontent.com/minelminel/microbot/master/microbot/install.sh | sudo bash
# 
set -e
REPO=microbot
cd $HOME

if [ ! -d ${HOME}/${REPO} ]; then
do
    git clone https://github.com/minelminel/${REPO}
    cd ${REPO}
else
    cd ${REPO}
    git pull origin master
fi

python3 -m pip install --upgrade pip setuptools wheel virtualenv

python3 -m virtualenv env
source env/bin/activate
pip install -r $(ls *requirements.txt)
pip install -e .
pytest

HOST=$(ifconfig wlan0 | grep 'inet ' | xargs | cut -d' ' -f2)
echo "HOST: $HOST"
