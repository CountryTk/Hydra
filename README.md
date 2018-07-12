# PyPad
A simple cross-platform text editor in python.


## Configuration
User config is stored in the configuration directory for your OS

Linux: `~/.config/PyPad/config.json`

Windows: `%appdata%/PyPad/config.json`

Mac OS: `~/Library/Application\ Support/PyPad/config.json`

The `config.json` in `pypad/resources` is default config that is copied to the above locations.
Editing it will have no effect, as it is only used as a fall back if a value cannot be found in the main configuration or is entirely missing.

## Screenshots

![Screenshot of PyPad](https://i.imgur.com/ksWUpA4.png)