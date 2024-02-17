#!/usr/bin/env bash

# kill any servers that may be running in the background
sudo pkill -f runserver

# kill frontend servers if you are deploying any frontend
# sudo pkill -f tailwind
# sudo pkill -f node

cd /home/ubuntu/Team3-Book-Management-BE/

# activate virtual environment
python3 -m venv venv
source venv/bin/activate

install requirements.txt
pip install -r requirements.txt

# run server
cd /backend
python3 manage.py makemigrations 
python3 manage.py migrate
screen -d -m python3 manage.py runserver 0:8000