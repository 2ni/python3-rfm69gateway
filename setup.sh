#!/bin/bash
sudo apt install python3-venv python3-rpi.gpio
git clone git@github.com:2ni/python3-rfm69gateway.git
cd python3-rfm69gateway
git submodule update --init --recursive
git submodule update --recursive --remote  # to update submodules
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
