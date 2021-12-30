#!/bin/bash

echo "Copying source and config files into tmp dir..."
rsync -avr --exclude '__pycache__' ../src/* tmp
rsync -avr ../$1 tmp

echo "Creating virtual env..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies into tmp dir..."
pip3 install -r ../requirements.txt -t tmp
