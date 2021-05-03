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
if [ ! -d ${HOME}/${REPO}/env ]; then
do
    echo "Creating new virtual environment"
    python3 -m virtualenv env
fi
source env/bin/activate
pip install -r $(ls *requirements.txt)
pip install -e .
pytest

# Create a config file if none exists, using the example
if [ -f config.json ]; then
do
    echo "Creating configuration file"
    cp example-config.json config.json
fi

HOST=$(ifconfig wlan0 | grep 'inet ' | xargs | cut -d' ' -f2)
echo "HOST: $HOST"
