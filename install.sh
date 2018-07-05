#!/bin/bash

INSTALL_DIR="$HOME/pypad/"
PYPAD_DIR="/usr/bin/pypad"
MAIN_DIR="/opt/pypad"



function main() {
        echo "Creating filestructure for pypad"
        echo " "
        echo "Installing"
        run_structure >> /var/log/pypad.log
        echo "All done. Cleaning up. Remove install.sh and directory manually for now."
        cleanup
}

function run_structure() {
        while true; do
                sudo touch /opt/pypad/
                sudo cp $INSTALL_DIR/* /opt/pypad
        done
}

function create_files() {
        sudo touch $PYPAD_DIR
        sudo chmod +x $PYPAD_DIR
        echo "python3 $HOME/pypad/main.py" >> $PYPAD_DIR
}

function cleanup() {
        sudo rm -rf $I
        find . ! - name '$INSTALL_DIR/install.sh' -type f -exec rm -f {} +
}


main
