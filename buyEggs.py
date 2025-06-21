from time import sleep  # To make sure each action is registered properly

import Constants.constantsPositions as constants
import window_actions as autoit
from buy import getMoneySymbol


def buyEggShop():
    """
    Automatically buys most items from the gear shop in the game.
    By default, it will buy the following items:
    - Recall Wrenches
    - All Sprinklers(Basic, Advanced, Godly, Master)
    - Lightning Rods

    This can be modifed in the Constants/constantsFilepaths.py file.
    """

    gotoGearShop()
    # hold s down for 1.2 seconds
    sleep(1)
    autoit.send("{w down}")  # Press and hold the 's' key
    sleep(1.4)  # Hold for 1.2 seconds
    autoit.send("{w up}")  # Release the 's' key
    sleep(0.75)
    autoit.send("{e}")  # Press the 'e' key to open the egg shop
    sleep(0.2)
    coords = getMoneySymbol()
    if coords is not None:
        sleep(0.2)
        autoit.click_absolute(
            coords[0], coords[1]
        )  # Click the money symbol to ensure we have enough money

    sleep(0.5)  # Wait for the egg shop to open
    autoit.send("{w down}")  # Press and hold the 's' key
    sleep(0.2)  # Hold for 1.2 seconds
    autoit.send("{ws up}")  # Release the 's' key
    sleep(0.75)
    autoit.send("{e}")  # Press the 'e' key to open the egg shop
    sleep(0.5)
    coords = getMoneySymbol()
    if coords is not None:
        sleep(0.2)
        autoit.click_absolute(coords[0], coords[1])

    autoit.send("{w down}")  # Press and hold the 's' key
    sleep(0.2)  # Hold for 1.2 seconds
    autoit.send("{w up}")  # Release the 's' key
    sleep(0.75)
    autoit.send("{e}")  # Press the 'e' key to open the egg shop
    sleep(0.5)
    coords = getMoneySymbol()
    if coords is not None:
        sleep(0.2)
        autoit.click_absolute(coords[0], coords[1])
    autoit.closeGui()


def gotoGearShop():
    autoit.send(
        constants.recallWrenchKeybind
    )  # Player holds the recall wrench in their hand
    autoit.click(
        "left"
    )  # Player uses the recall wrench to teleport to the gear shop    autoit.click("left")  # Player uses the recall wrench to teleport to the gear shop
