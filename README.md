# PyPad
A simple cross-platform python editing notepad written in python.

This editor is fully customizable, just edit the config.json file. All color codes  **MUST** be hex color codes!

Required modules: PyQt5, pyautogui

**If you use MacOs and can't install pyautogui follow this**

https://stackoverflow.com/questions/35074294/pip3-install-pyautogui-fails-with-error-code-1-mac-os

Tab width is set to 45 which acts as 4 spaces.

![alt text](https://raw.githubusercontent.com/Fuchsiaff/csgo_wallhack/master/2018-06-04-174804_1920x1025_scrot.png)

## Config

Config is done via `config.json` in root repository directory.
Example config:

```json
{
  "editor": [
    {
      "windowStaysOnTop": false,

      "editorFont": "Iosevka",

      "editorFontSize": 12,

      "editorColor": "#303030",

      "windowColor": "#303030",

      "windowText": "#36fc0a",

      "alternateBase": "#FFFFFF",

      "ToolTipBase": "#FFFFFF",

      "ToolTipText": "#FFFFFF",

      "editorText": "#FFFFFF",

      "buttonColor": "#353535",

      "buttonTextColor": "#FFFFFF",

      "HighlightColor": "#4DD2FF",

      "HighlightedTextColor": "#000000",

      "TabWidth": 45,

      "DontUseNativeDialog": false

    }
  ],
  "syntaxHighlightColors": [
    {
      "keywordFormatColor": "#0099FF",

      "classFormatColor": "#00FF16",

      "functionFormatColor": "#FF9500",

      "quotationFormatColor": "#039135",

      "magicFormatColor": "#ff6666",

      "decoratorFormatColor": "#ff00e7",

      "intFormatColor": "#70DBFF"

    }
  ]
}
```
