import os
import curses

def list_folders(directory):
    folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    return folders

def choose_folder(stdscr, directory):
    curses.curs_set(0)  # Hide the cursor
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Define color pair

    folders = list_folders(directory)
    current_row = 0

    while True:
        stdscr.clear()

        for i, folder in enumerate(folders):
            color = curses.color_pair(1) if i == current_row else curses.A_NORMAL
            stdscr.addstr(i, 0, f"{i + 1}. {folder}", color)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(folders) - 1:
            current_row += 1
        elif key == 10:  # Enter key
            return os.path.join(folders[current_row])


