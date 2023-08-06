"""
Code for subscription list.

functions:
    add_channel
    get_channels
"""
#!/usr/bin/env python3

from os.path import isfile
from re import search
from config import _CHANNEL_FILE
from storage import get_data, save_data


def validate_link(url: str) -> bool:
    """Validate if a link given is valid or not.

    arguments:
        url

    return:
        None
    """
    match = search("^https://www.youtube.com/c/\w+/\w+$", url)
    if match == None:
        return False
    else:
        return True


def add_channel(url: str) -> bool:
    """Add a channel to the list.

    arguments:
        url - channel url

    return:
        None
    """
    channels = []
    if isfile(_CHANNEL_FILE):
        channels = get_data(_CHANNEL_FILE)
    channel = url.split('/')[-2]
    if channel not in channels:
        channels.append(channel)
        save_data(_CHANNEL_FILE, channels)
        return True
    return False


def get_channels() -> list:
    """Get the list of channels suscribed.

    return:
        [channels]
    """
    return get_data(_CHANNEL_FILE)


if __name__ == '__main__':
    print(get_channels())
