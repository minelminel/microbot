#!/usr/bin/env bash
set -e

sudo apt-get install -y nginx
sudo cp ./microbot.* /etc/systemd/system/
sudo cp ./nginx.conf /etc/nginx/nginx.conf
sudo systemctl enable --now microbot.service
sudo systemctl enable --now nginx.service
curl localhost:8000
