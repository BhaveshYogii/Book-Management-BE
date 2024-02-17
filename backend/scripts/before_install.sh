#!/usr/bin/env bash


# update os & install python3 and libpq-dev for postgresql


cd home/ubuntu/Team3-Book-Management-BE
sudo apt-get update
sudo apt-get install -y python3 python3-dev python3-pip python3-venv libpq-dev
pip install --user --upgrade virtualenv

# delete app
sudo rm -rf /home/ubuntu/Team3-Book-Management-BE/