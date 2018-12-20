
def checkVersion(file):
    
    with open(file, "r") as f:
        version = f.read()
    return str(version)

