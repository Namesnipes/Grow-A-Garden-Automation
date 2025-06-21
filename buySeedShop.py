# For debugging purposes, you can uncomment the following import statements:

from time import sleep

import Constants.constantsFilepaths as filepaths
import Constants.constantsPositions as constants
import window_actions as autoit
from buy import buy


def buySeedShop():
    """
    Automatically buys most items from the gear shop in the game.
    By default, it will buy all seeds from Divine rarity and up, as well as Mango and Grape seeds.

    This can be modifed in the Constants/constantsFilepaths.py file.
    """

    seedsToBuy = list(filepaths.seedShopItemTemplatePaths)

    if moveToSeedShop():  # Ensure player is in the seed shop before buying items
        buy(seedsToBuy)  # Buy the items from the seed shop
        autoit.closeGui()  # Close the seed shop after buying items

    else:
        print("Failed to open the seed shop. Please check your settings and try again.")


def moveToSeedShop():
    """
    Moves the player to the seed shop.
    This function should be called before buying seeds.
    """

    autoit.move(constants.seedsButtonPosX, constants.seedsButtonPosY)
    autoit.click("left")  # Click the seeds button to open the seed shop
    sleep(0.5)  # Wait for the teleport animation to finish
    autoit.send("e")  # Player interacts with the gear shop to open it
    sleep(0.2)
    autoit.send("e")
    autoit.click_window_center(
        False
    )  # Move mouse to the center of the screen to focus on the shop window
    sleep(1.5)  # Wait for seed shop vendor to open seed shop
    # TODO: check if seed shop is open
    return True
