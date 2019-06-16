import os

last_file = ['resources/lastFile.txt']


def update_previous_file(filepath=last_file[0]):
    try:
        if os.path.isfile(filepath):
            try:
                with open(last_file[0], 'w+') as file:
                    file.write(filepath)
            except (FileNotFoundError, IOError) as err:
                print(err)
                return False
    except Exception as err:
        print(err)
        return False


def get_last_file():
    try:
        if os.path.isfile(last_file[0]):

            try:
                with open(last_file[0], 'r') as file:
                    contents = file.read()
                    if os.path.isfile(contents):

                        return contents
                    else:
                        return None
            except (FileNotFoundError, IOError) as err:
                print(err)
                return False
    except Exception as err:
        print(err)
        return False
