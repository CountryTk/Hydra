
def updateLastFileOpen(filepath):
    """
        Updates the path in the file that stores the last file edited with PyPad
        If this config file can't be accessed for any reason it returns False
    """
    try:
        open(filepath, 'r').close()
    except FileNotFoundError:
        return False

    with open('resources/lastFile.txt', 'w') as f:
        f.write(filepath)
    return True


def lastFileOpen():
    """
        Returns the path to the last file edited with PyPad
        If this filepath can't be accessed for any reason it returns None
    """
    try:
        # Path to last file opened is kept in special config file
        with open('resources/lastFile.txt', 'r') as f:
            filepath = f.read().strip()

        # Check file will open
        open(filepath, 'r').close()

        return filepath

    # If ethier open fails return none
    except FileNotFoundError:
        print('last-file-open config file not found')
        return None
