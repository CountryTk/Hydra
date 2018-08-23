# PyPad
A simple cross-platform python editing notepad with auto completion and the ability to run scripts in interactive mode, written in python.

This editor is very customizable, just edit the config.json file. All color codes  **MUST** be hex color codes!

Required modules: PyQt5, urxvt terminal emulator. 

# Installation with install.sh
```sudo -i```

```cd /root (if you're not in /root directory already```

```mkdir pypad && cd pypad```

```git init && git pull https://github.com/Fuchsiaff/PyPad```

```chmod +x install.sh```

```./install.sh (When it prompts for home directory, use "/root" no quotations)```

If you get a ^M markdown error when running use ```dos2unix install.sh``` to convert.

# How to use when installation fails
```git clone https://github.com/Fuchsiaff/PyPad```
```cd PyPad && cd src```
```python3 main.py```

![alt text](https://raw.githubusercontent.com/Fuchsiaff/as/master/2018-07-10-221615_800x665_scrot.png)
