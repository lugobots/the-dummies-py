#!/bin/bash

echo "Building bot image"
cd .lugo || exit 1
echo " - Installing hot load watcher"
npm install -g nodemon@3.0.1 > /dev/null

cd /app || exit 2

if [ ! -d ".lugo/venv" ]; then
  echo " - Installing Python Environment"
  pip install virtualenv || exit 3
  virtualenv .lugo/venv --python=python3.9  || exit 4
  chmod +xw -R .lugo/venv
fi

echo " - Installing Python requirements"
source .lugo/venv/bin/activate
pip install -q -r requirements.txt
#chmod 777 -R .lugo/venv