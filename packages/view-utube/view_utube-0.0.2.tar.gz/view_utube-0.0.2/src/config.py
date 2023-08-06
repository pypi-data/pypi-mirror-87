"""Configuration file."""
#!/usr/bin/env python3

from os.path import expanduser
from curses import A_BOLD, A_STANDOUT

# program to handle the youtube video link
# change it to the program of your choice
_LINK_HANDLER = 'utlh'

# default file path
_BASE_DIR = f'{expanduser("~")}/.local/utube/'
_CHANNEL_FILE = _BASE_DIR + 'channels.txt'
_DATA_FILE = _BASE_DIR + 'data.txt'

# constants for youtube link path
_BASE_YT_URL = 'https://www.youtube.com/'
_CHANNEL_VIDEO_START = _BASE_YT_URL + 'c/'
_CHANNEL_VIDEO_END = '/videos'
_BASE_YT_WATCH_URL = _BASE_YT_URL + 'watch?v='

# constant for ncurses
_HIGHLIGHT = A_BOLD | A_STANDOUT
