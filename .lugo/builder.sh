#!/usr/bin/env bash

cd .lugo || exit 1
npm install -g nodemon@3.0.1

cd /app || exit 2

if [ ! -d ".lugo/venv" ]; then
  pip install virtualenv || exit 3
  virtualenv .lugo/venv --python=python3.9  || exit 4
fi

chmod +xw -R .lugo/venv
source .lugo/venv/bin/activate
pip install -r requirements.txt
#chmod 777 -R .lugo/venv