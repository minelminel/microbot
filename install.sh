#!/usr/bin/env bash
# 
# RASPBERRY PI INSTALLATION SCRIPT
# 
# curl https://raw.githubusercontent.com/minelminel/microbot/master/install.sh | sudo bash
# 
set -e

main() {
    REPO=microbot

    if [ ! -d "${HOME}/${REPO}" ]; then
        git clone "https://github.com/minelminel/${REPO}"
        cd "${HOME}/${REPO}"
    else
        cd "${HOME}/${REPO}"
        git pull origin master
    fi

    python3 -m pip install --upgrade pip setuptools wheel virtualenv
    if [ ! -d "${HOME}/${REPO}/env" ]; then
        echo "Creating new virtual environment"
        python3 -m virtualenv env
    fi
    source env/bin/activate
    echo "CWD: $(pwd)"
    find . -type f -name "*requirements.txt" -print | xargs -n1 pip install -r
    pip install -e .
    pytest

    # Create a config file if none exists, using the example
    if [ -f config.json ]; then
        echo "Creating configuration file"
        cp example-config.json config.json
    fi

    HOST=$(ifconfig wlan0 | grep 'inet ' | xargs | cut -d' ' -f2)
    echo "HOST: $HOST"
}

main
