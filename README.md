# PyPad
A simple cross-platform python IDE with auto completion and the ability to run scripts in interactive mode, written in python.

This editor is very customizable, just edit the config.json file. All color codes  **MUST** be hex color codes!

Required modules: PyQt5, bs4, lxml parser and qtconsole.

# Auto completion

Auto completion pops up by pressing Ctrl+Space. It will automatically reccommend the best word and pressing enter will select the word.

You can also navigate the word list with arrow keys.

# nltk installation
After doing pip install -r requirements.txt you need to open up a cmd/terminal and follow these steps:

```python```

```import nltk```

```nltk.download('punkt')```

# Search function

To use the search function, you first have to press Ctrl+F and then type in the word you want to search then press ok.
To cycle through any words that were found, you press F3

# Installation
```git clone https://github.com/Fuchsiaff/PyPad.git && cd PyPad && pip install -r requirements.txt && cd src && python main.py``` 
