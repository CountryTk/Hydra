from nltk.tokenize import word_tokenize


def tokenize(file):
    classNames = []
    varNames = []
    functionNames = []
    ignore = ["(", ")", "[", "]", "{", "}", "#", "@", "!", "*"]
    try:
        with open (file, 'r') as openedFile:
            list = word_tokenize(openedFile.read())
  
        for index, names in enumerate(list):
        
            if list[index] == "def":
                if list[index + 1] not in functionNames:
                    functionNames.append(list[index + 1])
                
            if list[index] == "class": 
                if list[index + 1] not in classNames:
                    classNames.append(list[index + 1])
                
            if list[index] == "=":
                if list[index - 1] not in classNames and list[index - 1] not in ignore:
                    varNames.append(list[index - 1])
                         
        return (classNames, varNames, functionNames)
    except (FileNotFoundError, UnboundLocalError) as E:
        return ("", "", "")

