from time import sleep

import window_actions as autoit
from moveTo import gotoSell


def makeHoney():
    """
    This function simulates the process of making honey.
    It returns a string indicating that honey has been made.
    """
    gotoSell()
    # click middle
    autoit.click_window_center()  # Click the middle of the screen to focus the game window
    # hold down d for 10 seconds
    autoit.send("{d down}")  # Press and hold the 'd' key
    sleep(7.8)  # Hold for 10 seconds
    autoit.send("{d up}")  # Release the 'd' key
    # hold w for 250 ms
    autoit.send("{s down}")  # Press and hold the 'w' key
    sleep(0.7)  # Hold for 250 milliseconds
    autoit.send("{s up}")  # Release the 'w' key
    sleep(0.5)  # Wait for the animation to finish
    autoit.send("{e}")
    # press backtick
    autoit.send("`")  # Press the backtick key to open the chat
    sleep(0.5)  # Wait for the chat to open
    # c;lick 1146, 671
    autoit.click("left", 631, 230)  # Click the honey button
    # ctral a backspace then type polinated
    autoit.send("{CTRLDOWN}a{CTRLUP}")  # Select all text in the chat
    sleep(0.2)
    autoit.send("{BACKSPACE}")  # Clear the chat input
    sleep(0.2)  # Wait for the backspace to clear the input
    autoit.send("pollinated")  # Type the word "pollinated"``
    # click 672, 722 todo change
    sleep(0.5)
    for i in range(3):
        autoit.click("left", 109, 279)  # Click the item in inventory
        sleep(0.8)
        autoit.send("{e}")  # Press the 'e' key to confirm the honey making
        sleep(0.8)
    autoit.send("`")  # Press the backtick key to open the chat
    sleep(0.5)
