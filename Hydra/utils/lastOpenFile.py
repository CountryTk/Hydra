import os

last_file = ["resources/lastFile.txt"]


def update_previous_file(filepath):
    try:
        if os.path.isfile(filepath):
            try:
                with open("resources/lastFile.txt", "w+") as file:
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
                with open(last_file[0], "r+") as file:
                    return file.read(
                        50
                    )  # Might need to assign more bytes if it reaches limit.
            except (FileNotFoundError, IOError) as err:
                print(err)
                return False
    except Exception as err:
        print(err)
        return False
