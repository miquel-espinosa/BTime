#!/bin/bash

## Instal requirements
pip3 install -r requirements.txt

## Set execution to main.py
chmod +x main.py

## Symbolic link instead of bashrc alias
sudo ln -sf $(realpath main.py) /usr/local/bin/btime


