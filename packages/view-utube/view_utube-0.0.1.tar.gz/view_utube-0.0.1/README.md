# utube
Simple TUI app to watch suscribed youtube channel videos.

## Table of contents
* [Info](#Info)
* [Technologies](#Technologies)
* [Usage](#Usage)
* [Controls](#Controls)

## Info
**utube** is a basic TUI application to watch youtube videos. Just add the channel links you want to watch, and you are ready to go.

## Technologies
Built in python3 with *curses*.

### Dependencies:
* [![scraper: gazpacho](https://img.shields.io/badge/scraper-gazpacho-C6422C)](https://github.com/maxhumber/gazpacho) - scrape and parse youtube pages

## Usage
```python

  # install
  pip install utube

  # run
  utube
```


## Controls
* **j**   Move UP
* **k**   Move DOWN
* **g**   Move to TOP
* **G**   Move to BOTTOM
* **a**   Add channel
* **l**   Enter sub-menu
* **h**   Exit sub-menu
* **q**   Quit
