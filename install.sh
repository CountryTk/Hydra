#!/bin/bash

PYPAD_GIT="https://github.com/Fuchsiaff/PyPad"

function main() {
        if [ ! -f /usr/bin/git ]; then
                echo "Git not found in /usr/bin. Aborting"
                exit 1
		elif [ ! -d /opt/pypad/ ]; then
				mkdir /opt/pypad/ && touch /opt/pypad/.git
				pull_pypad
		elif [ -d /opt/pypad ] && [ -d /opt/pypad/.git ]; then
				cd /opt/pypad | pull_pypad
		else 
				echo "Install failed"
		fi
        
}

function pull_pypad() {
	git pull $PYPAD_GIT
}

main

