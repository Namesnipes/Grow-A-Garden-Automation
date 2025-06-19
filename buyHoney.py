from time import sleep

from buy import buy
from moveTo import gotoSell
import Constants.constantsFilepaths as filepaths
import window_actions as autoit

def buyHoney():
    """
    This function simulates the process of making honey.
    It returns a string indicating that honey has been made.
    """
    gotoSell()
    #click middle
    autoit.click("left", 960, 540)  # Click the middle of the screen to focus the game window
    #hold down d for 10 seconds
    autoit.send("{d down}")  # Press and hold the 'd' key
    sleep(9.2)  # Hold for 10 seconds
    autoit.send("{d up}")  # Release the 'd' key
    # hold w for 250 ms
    autoit.send("{s down}")  # Press and hold the 'w' key
    sleep(1)  # Hold for 250 milliseconds
    autoit.send("{s up}")  # Release the 'w' key
    sleep(0.5)  # Wait for the animation to finish
    autoit.send("{e}")
    # press backtick
    honeyToBuy = list(filepaths.honeyShopItemTemplatePaths)
    buy(honeyToBuy)
    autoit.closeGui()