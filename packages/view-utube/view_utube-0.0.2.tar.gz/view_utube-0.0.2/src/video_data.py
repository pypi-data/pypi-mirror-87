"""
Code to save and extract video info.

functions:
    save_video_info
    get_video_info
"""
#!/usr/bin/env python3

from config import _DATA_FILE
from storage import get_data, save_data


def save_video_info(parsed_data: list) -> None:
    """Save the video info.

    arguments:
        parsed_data

    return:
        None
    """
    save_data(_DATA_FILE, parsed_data)

def get_video_info() -> any:
    """Get the video info.

    return:
        video-info
    """
    return get_data(_DATA_FILE)


def get_video_list(channel: str) -> list:
    """Get the video list of channel.

    arguments:
        channel

    return:
        [video data]
    """
    video_list = get_video_info()
    return video_list[channel]


if __name__ == '__main__':
    print(get_video_info())
