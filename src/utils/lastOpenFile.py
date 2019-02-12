import os


def updateLastFileOpen(filepath):
    try:
        os.path.isfile(filepath)
    except (FileNotFoundError, PermissionError, OSError):
        return False

    with open('resources/lastFile.txt', 'w') as f:
        f.write(filepath)
    return True


def lastFileOpen():
    try:
        file = open('resources/lastFile.txt', 'r+')
        try:
            return file.read().strip()
        finally:
            file.close()
    except (FileNotFoundError, PermissionError, OSError):
        print('last-file-open config file not found')
        return None
