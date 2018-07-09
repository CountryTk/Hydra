#!/bin/bash

INSTALL_DIR=""
NOHUP_DIR="/var/log/nohup.out"
PYPAD_DIR="/usr/bin/pypad"
MAIN_DIR="/opt/pypad"

function main() {
        read -p "Enter home directory full path: " INSTALL_DIR
        echo "Creating filestructure for pypad"
        echo " "
        echo "Installing via nohup background process"
        nohup run_structure &> NOHUP_DIR
        wait $!
        echo "All done. Cleaning up. Removing old directories."
        nohup create_files &> NOHUP_DIR
        wait $!
        nohup cleanup &> NOHUP_DIR
        echo "Use: cat $NOHUP_DIR to read output."
        exit 1
}

function run_structure() {
        mkdir /opt/pypad/
        cp -r $INSTALL_DIR/pypad  /opt/
}

function create_files() {
        touch $PYPAD_DIR
        chmod +x $PYPAD_DIR
        echo "sudo python3 $MAIN_DIR/src/main.py" > $PYPAD_DIR
}

function cleanup() {
        rm -rf $INSTALL_DIR/pypad/
}

main
