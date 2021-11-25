import curses
from curses import wrapper
from curses.textpad import rectangle
import time
import random


# Functions explained:
# .clear() - will empty a terminal.
# .refresh() - will print to a terminal all that has been added since the last refresh.
# .addstr() - accepts a 'y' and 'x' value and prints the third argument at y, x in the 4th argument colour.
# curses.init_pair() and curses.color_pair() allow a fore and background colour pair to be assigned.
# .curs_set() - 0 or 1 sets the cursor to visible or invisible.
# rectangle() - draws a rectangle to the terminal.
# .getch() - gets the ASCII value of the pressed key.


def main(stdscr):
    """Main body of program."""
    # Obtain the phrase that will be typed.
    possible_phrases = ['the quick brown fox jumped over the lazy dog', 'quicken the mixing of the cat soup',
                        'consider the many hazy elements at a distance', 'forthright and vexing in every sense',
                        'concatenate the sum of duplicate values within an array',
                        'come on england score some flippin goals', 'this is my first attempt at curses']

    phrase = random.choice(possible_phrases)
    phrase_len = len(phrase)

    # Initialise needed colours and assign to variables.
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    green_on_black = curses.color_pair(1)

    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    red_on_black = curses.color_pair(2)

    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
    white_on_red = curses.color_pair(3)

    # Greet the user.
    stdscr.clear()
    stdscr.addstr(0, 0, "Type-Speed Test Initialised...", green_on_black)
    stdscr.refresh()
    time.sleep(1.5)
    stdscr.addstr(2, 0, "You will be given a random phrase. Once you have typed it correctly\nyou will be"
                        "presented with your final 'WORDS PER MINUTE' score.\nPress 'F4' to exit.\n\n"
                        "Press any key to begin...")

    # Pause for user.
    stdscr.getch()

    # Clears terminal and sets cursor to 'invisible'.
    stdscr.clear()
    curses.curs_set(0)

    # Set the cancelled('quit') flag to False, this will only equal True if the user completes the word.
    cancelled = False

    # Gets the starting time and enables 'nodelay', so there is no waiting for user input.
    start_time = time.time()
    stdscr.nodelay(True)

    # Create empty string to store user's typed characters.
    draw_string = ''

    # If the phrase is not complete or the user has not pressed 'F4', we continue to loop and get user input.
    while True:
        # Determines what color to display the user input as.
        if phrase[:len(draw_string)] != draw_string:
            correct_so_far = False
        else:
            correct_so_far = True

        # Draws the phrase to type to the terminal in a box.
        rectangle(stdscr, 0, 0, 2, phrase_len+1)
        stdscr.addstr(1, 1, phrase, red_on_black)

        # Displays the user input in the appropriate colors.
        if correct_so_far:
            stdscr.addstr(1, 1, draw_string, green_on_black)
        else:
            stdscr.addstr(1, 1, draw_string, white_on_red)

        # Updates the terminal with all the above.
        stdscr.refresh()

        # If new user input is provided, we evaluate it in the if, elif, else block below.
        press = stdscr.getch()

        if len(draw_string) == phrase_len:
            if draw_string == phrase:
                break
            else:
                draw_string = draw_string[:-1]
                continue

        # 'Backspace'.
        if press == 8:
            draw_string = draw_string[:-1]

        # 'F4' or 'quit'.
        elif press == 268:
            cancelled = True
            break

        # 'Space'
        elif press == 32:
            draw_string += ' '

        # Not a valid 'special key' and not a valid letter.
        elif press < 97 or press > 122:
            continue

        # 'Lowercase letter'.
        else:
            draw_string += chr(press)
        stdscr.clear()

    # If the user has quit...
    stdscr.nodelay(False)
    if cancelled:
        stdscr.clear()
        stdscr.addstr(0, 0, "You quit!\nPress any key to exit...")
        stdscr.refresh()

    # If the user has completed the phrase...
    else:
        end_time = time.time()
        time_taken = end_time - start_time

        # Calculate WPM based on 4.7 characters per word.
        stdscr.addstr(4, 0, f"WPM: {int(60 * (len(phrase)/time_taken) / 4.7)}")

        stdscr.addstr(5, 0, "Nice job!")
        stdscr.addstr(6, 0, "Press any key to exit...")
        stdscr.refresh()

    # User must press a key to exit program.
    stdscr.getch()


if __name__ == '__main__':
    wrapper(main)
