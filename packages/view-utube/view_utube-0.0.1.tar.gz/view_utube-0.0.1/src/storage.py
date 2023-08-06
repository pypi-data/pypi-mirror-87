"""
Contains code to storage and retrieve data.

functions:
    save_data
    get_data
"""
#!/usr/bin/env python3

from os.path import isfile
from pickle import dump, load


def save_data(file_name: str, data: any) -> None:
    """Save data to file_name.

    arguments:
        file_name
        data

    return:
        None
    """
    with open(file_name, 'wb') as writer:
        dump(data, writer)


def get_data(file_name: str) -> any:
    """Extract data from file_name.

    arguments:
        file_name

    return:
        [data]
    """
    if not isfile(file_name):
        return []
    with open(file_name, 'rb') as reader:
        data = load(reader)
    return data


if __name__ == '__main__':
    pass
