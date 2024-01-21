import curses
from curses import wrapper
import json
from typing_test import TypingTest
import string


def print_menu(stdscr, title, menu_items, selected_row):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Print the menu title
    stdscr.addstr(0, w//2 - len(title)//2, title)

    # Print menu options
    for i, option in enumerate(menu_items):
        x = w//2 - len(option)//2
        y = h//2 - len(menu_items)//2 + i
        if i == selected_row:
            stdscr.addstr(y, x, option, curses.A_STANDOUT)
        else:
            stdscr.addstr(y, x, option)


def print_story(stdscr, user_input: str, story: str):
    i = 0
    # Color user input
    while i < len(user_input):
        stdscr.addstr(
            user_input[i],
            curses.color_pair(2) if user_input[i] == story[i]
            else curses.color_pair(1)
        )
        i += 1

    # Print remaining story
    stdscr.addstr(story[len(user_input):])
    stdscr.addstr('\n\n')


def start_test(stdscr, story):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    user_input = ''
    i = 0
    tst = TypingTest()

    stdscr.clear()
    print_story(stdscr, user_input, story)
    stdscr.addstr('Press Enter to start')
    stdscr.refresh()
    while stdscr.getch() not in (curses.KEY_ENTER, 10, 13):
        continue
    tst.start_timer()

    while len(user_input) < len(story):
        stdscr.clear()
        print_story(stdscr, user_input, story)
        stdscr.addstr(f'WPM: {tst.get_wpm(user_input)}\n')
        stdscr.addstr(
            f'Accuracy: {tst.measure_accuracy(user_input, story)}\n'
        )
        stdscr.addstr(
            f'Difficult Keys: {tst.difficult_keys(user_input, story)}\n'
        )
        stdscr.addstr(f'Time Taken: {tst.time_taken()}')
        stdscr.refresh()

        ch = stdscr.getch()
        if chr(ch) in string.printable:
            user_input += chr(ch)
        elif ch == curses.KEY_BACKSPACE:
            user_input = user_input[:-1]
        i += 1

    stdscr.addstr('\nPress Enter to exit')
    stdscr.refresh()
    while stdscr.getch() not in (curses.KEY_ENTER, 10, 13):
        continue


def select_story(stdscr, menu_items):
    curses.curs_set(0)
    current_row = 0

    while True:
        print_menu(stdscr, "Select a story", menu_items, current_row)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return current_row


def main():
    with open('stories.json') as f:
        stories = json.load(f)['stories']
    stories = sorted(stories, key=lambda x: x['title'])

    titles = [story['title'] for story in stories]
    selected_index = curses.wrapper(select_story, titles + ['Exit'])
    if selected_index == len(titles):
        return

    story = stories[selected_index]['content']
    wrapper(start_test, story)


if __name__ == '__main__':
    main()
