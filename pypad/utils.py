def flatten(d: dict, parent_key: str='', sep: str='.'):
    """
    Flatten a dictionary into a single set of keys and values
    :param d: dictionary to flatten
    :param parent_key: value to append to the front of the new key
    :param sep: separator between old keys in the new key
    :return: the flat dictionary
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def merge(first: dict, second: dict):
    """
    Combine the values of two multi level dictionaries
    :param first: initial dictionary
    :param second: dictionary whose values overwrite the first
    :return: the combined dictionary
    """
    for key, value in first.items():
        if key in second:
            if isinstance(value, dict):
                first[key] = merge(value, second[key])
            else:
                first[key] = second[key]
    for key, value in second.items():
        if key not in first:
            first[key] = value
    return first


def make_list(value):
    """
    make a variable into a list if not already
    :param value: variable to be put into a list
    :return: list containing variable
    """
    return [value] if not isinstance(value, list) else value
