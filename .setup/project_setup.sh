#!/bin/bash

if [ -z "$(ls -A .)" ]; then
   if ! git clone -q https://github.com/lugobots/the-dummies-py.git
   then
     echo "fail to clone the repo :-("
     exit
   fi
   cd the-dummies-py
   LATEST_VERSION=$(git describe --tags $(git rev-list --tags --max-count=1))
   echo "Latest version: "$LATEST_VERSION
   if [ -z "$VERSION" ]
   then
         INSTALL_VERSION=$LATEST_VERSION
   else
         INSTALL_VERSION=$VERSION
   fi
   git fetch --all --tags -q
   git checkout -q tags/$INSTALL_VERSION
   echo "Installing The Dummmies Py Verion "$INSTALL_VERSION
   cd ..
   mv the-dummies-py/* .
   rm -rf the-dummies-py
   echo "All done! Please fix the file permissions running:
   On Linux or Mac: chown x:x -R ."
else
   echo "The output directory must be empty"
fi

