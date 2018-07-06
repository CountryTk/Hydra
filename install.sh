#!/bin/bash

INSTALL_DIR=""
PYPAD_DIR="/usr/bin/pypad"
MAIN_DIR="/opt/pypad"

function main() {
        read -p "Enter home directory full path: " INSTALL_DIR
        echo "Creating filestructure for pypad"
        echo " "
        echo "Installing"
        run_structure >> /var/log/pypad.log
        echo "All done. Cleaning up. Remove install.sh and directory manually for now."
        create_files
        cleanup
        exit
}

function run_structure() {
        mkdir /opt/pypad/
        cp -r $INSTALL_DIR/pypad  /opt/
}

function create_files() {
        touch $PYPAD_DIR
        chmod +x $PYPAD_DIR
        echo "python3 $MAIN_DIR/src/main.py" > $PYPAD_DIR
}

function cleanup() {
        rm -rf $INSTALL_DIR/pypad/
}

main
