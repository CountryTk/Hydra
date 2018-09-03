# PyPad
A simple cross-platform python editing notepad with auto completion and the ability to run scripts in interactive mode, written in python.

This editor is very customizable, just edit the config.json file. All color codes  **MUST** be hex color codes!

Required modules: PyQt5, bs4,lxml parser and qtconsole.
# Auto completion

Auto completion pops up by pressing Ctrl+Space. It will automatically reccommend the best word and pressing enter will select the word.

You can also navigate the word list with arrow keys.

# Installation with install.sh

```wget 

```./install.sh (When it prompts for home directory, use "/root" no quotations)```

If you get a ^M markdown error when running use ```dos2unix install.sh``` to convert.

# How to use when installation fails

```sudo pip install -r requirements.txt```

```git clone https://github.com/Fuchsiaff/PyPad cd PyPad && cd src && python main.py```

# Pictures

![alt text](https://raw.githubusercontent.com/Fuchsiaff/as/master/pypadpic.gif)

![alt text](https://raw.githubusercontent.com/Fuchsiaff/as/master/pypadpic2.gif)
