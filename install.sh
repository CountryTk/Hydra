#!/bin/bash

PYPAD_GIT="https://github.com/Fuchsiaff/PyPad"
PYPAD_PATH="/opt/pypad"

function main() {
        if [ ! -f /usr/bin/git ]; then
                echo "Git not found in /usr/bin/ - Aborting"
                exit 1

        elif [ ! -d $PYPAD_PATH ]; then
                clone_pypad
        else
                echo "Install failed"
        fi
}

function clone_pypad() {
        git clone $PYPAD_GIT $PYPAD_PATH
}

main


