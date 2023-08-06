"""A TUI app to watch youtube videos of suscribed channels."""
#!/usr/bin/env python3

from curses import wrapper, curs_set, init_pair, color_pair
from curses import echo, noecho
from curses import COLOR_BLACK, COLOR_YELLOW, COLOR_CYAN
from locale import setlocale, LC_ALL
from subprocess import run
from channel import get_channels, add_channel, validate_link
from config import _HIGHLIGHT, _LINK_HANDLER, _BASE_YT_WATCH_URL
from scrape import parse_channels
from video_data import get_video_list

setlocale(LC_ALL, '')


def execute_action(stdscr, c, current, length):
    """Handle key presses."""
    if c == ord('q'):
        quit()
    elif c == ord('g'):
        current = 0
    elif c == ord('G'):
        current =  length - 1
    elif c == ord('j'):
        current += 1
        if current == length:
            current -= 1
    elif c == ord('k'):
        current -= 1
        if current == -1:
            current = 0
    elif c == ord('a'):
        load_add_channel_menu(stdscr)
    elif c == ord('r'):
        load_refresh_menu(stdscr)
    return current

def print_channel_info(stdscr, data, current):
    """Print channel info."""
    rows, cols = stdscr.getmaxyx()
    stdscr.addstr(0, 0, f'{"Channel":<{cols}}', color_pair(1) | _HIGHLIGHT)
    for i, c in enumerate(data):
        channel_str = f'{c:<{cols}}'
        if i == current:
            stdscr.addstr(i + 1, 0, channel_str, color_pair(2) | _HIGHLIGHT)
        else:
            stdscr.addstr(i + 1, 0, channel_str)
    col = int(cols / 3)
    s_bar = f'{"q: Quit":<{col}}{"a: Add channel":<{col}}{"r: Refresh":<{col}}'
    stdscr.addstr(rows - 2, 0, f'{s_bar:<{cols}}', color_pair(1) | _HIGHLIGHT)


def print_video_info(stdscr, data, current):
    """Print video info."""
    rows, cols = stdscr.getmaxyx()
    col = int(cols / 10)
    rem = int(cols - 3 * col)
    header = f'{"Date":>{col}}{"Time":>{col}}{" "*col}{"Title":<{rem}}'
    stdscr.addstr(0, 0, header, color_pair(1) | _HIGHLIGHT)
    for i, v in enumerate(data):
        s = f'{v["date"]:>{col}}{v["time"]:>{col}}{" "*col}{v["name"]:<{rem}}'
        if i == current:
            stdscr.addstr(i + 1, 0, s, color_pair(2) | _HIGHLIGHT)
        else:
            stdscr.addstr(i + 1, 0, s)
    stdscr.addstr(rows - 2, 0, f'{"":<{cols}}', color_pair(1) | _HIGHLIGHT)



def show_list(stdscr, print_func, data, current):
    """Print the entries for the given data."""
    stdscr.clear()
    print_func(stdscr, data, current)
    stdscr.refresh()


def load_refresh_menu(stdscr):
    """Refresh the video data."""
    rows, cols = stdscr.getmaxyx()
    status = f'{"Please wait..":<{cols}}'
    stdscr.addstr(rows - 2, 0, status, color_pair(1) | _HIGHLIGHT)
    stdscr.refresh()
    parse_channels()


def load_add_channel_menu(stdscr):
    """Show Add channel menu."""
    rows, cols = stdscr.getmaxyx()
    curs_set(True)
    echo()
    stdscr.addstr(rows - 2, 0, f'{" ":{cols}}', color_pair(1) | _HIGHLIGHT)
    stdscr.addstr(rows - 2, 0, f'channel url: ', color_pair(1) | _HIGHLIGHT)
    stdscr.refresh()
    url = (stdscr.getstr()).decode()
    if validate_link(url):
        if add_channel(url):
            text = f'{"channel added. press any key to continue...":<{cols}}'
        else:
            text = f'{"channel exists. press any key to continue...":<{cols}}'
    else:
        text = f'{"invalid link. press any key to continue...":<{cols}}'
    stdscr.addstr(rows - 2, 0, text, color_pair(1) | _HIGHLIGHT)
    stdscr.refresh()
    stdscr.getch()
    noecho()
    curs_set(False)
    pass


def load_video_list_menu(stdscr, channel):
    """Show the video list menu."""
    videos = get_video_list(channel)
    length = len(videos)
    current = 0
    show_list(stdscr, print_video_info, videos, current)

    while True:
        c = stdscr.getch()
        if c == ord('h'):
            return
        if c == ord('l'):
            video_url = _BASE_YT_WATCH_URL + videos[current]['id']
            process = _LINK_HANDLER + ' ' + video_url
            run([process], shell=True)
        else:
            current = execute_action(stdscr, c, current, length)
        show_list(stdscr, print_video_info, videos, current)


def load_home_menu(stdscr):
    """Show the home menu."""
    channels = get_channels()
    length = len(channels)
    current = 0
    show_list(stdscr, print_channel_info, channels, current)

    while True:
        c = stdscr.getch()
        if c == ord('l'):
            load_video_list_menu(stdscr, channels[current])
        else:
            current = execute_action(stdscr, c, current, length)
        show_list(stdscr, print_channel_info, channels, current)


def ncurses_defaults() -> None:
    """Set basic defaults for ncurses."""
    curs_set(False)
    init_pair(1, COLOR_YELLOW, COLOR_BLACK)
    init_pair(2, COLOR_CYAN, COLOR_BLACK)


def start_app(stdscr) -> None:
    """Function wrapper."""
    ncurses_defaults()
    load_home_menu(stdscr)


def main() -> None:
    """Start the program."""
    wrapper(start_app)


if __name__ == '__main__':
    main()
