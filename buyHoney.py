import datetime
from time import sleep

import cv2
import numpy as np
from PIL import ImageGrab

import Constants.constantsFilepaths as filepaths
import window_actions as autoit
from buy import buy
from Constants import constantsPositions
from locateTemplateOnScreen import getColorOnScreen, locateTemplateOnScreen
from moveTo import gotoSell


def buyHoneyShop():
    """
    Automatically buys most items from the gear shop in the game.
    By default, it will buy the following items:
    - Recall Wrenches
    - All Sprinklers(Basic, Advanced, Godly, Master)
    - Lightning Rods

    This can be modifed in the Constants/constantsFilepaths.py file.
    """

    honeyToBuy = list(filepaths.honeyShopItemTemplatePaths)

    # If you plan to be in the gear shop for a long time, you can uncomment the line below to not use the recall wrench
    if moveToHoneyShop():  # Ensure player is in the gear shop before buying items
        buy(
            honeyToBuy, lambda: getColorOnScreen("26ee26")
        )  # Buy the items from the gear shop
        autoit.closeGui()  # Close the gear shop after buying items

    else:
        print("Failed to open the gear shop. Please check your settings and try again.")


def moveToHoneyShop():
    """
    This function simulates the process of making honey.
    It returns a string indicating that honey has been made.
    """
    gotoSell()
    # click middle
    autoit.click_window_center()  # Click the middle of the screen to focus the game window
    # hold down d for 10 seconds
    autoit.send("{d down}")  # Press and hold the 'd' key
    sleep(7.45)  # Hold for 10 seconds
    autoit.send("{d up}")  # Release the 'd' key
    # hold w for 250 ms
    autoit.send("{s down}")  # Press and hold the 'w' key
    sleep(0.7)  # Hold for 250 milliseconds
    autoit.send("{s up}")  # Release the 'w' key
    sleep(0.5)  # Wait for the animation to finish
    autoit.send("{e}")
    sleep(2)

    TL = autoit.convert_absolute_to_client_coords(
        constantsPositions.gearShopOptionsPosX1, constantsPositions.gearShopOptionsY1
    )
    BR = autoit.convert_absolute_to_client_coords(
        constantsPositions.gearShopOptionsPosX2, constantsPositions.gearShopOptionsY2
    )
    print(
        "absolute coords:",
        constantsPositions.gearShopOptionsPosX1,
        constantsPositions.gearShopOptionsY1,
        constantsPositions.gearShopOptionsPosX2,
        constantsPositions.gearShopOptionsY2,
    )
    print(f"TL: {TL}, BR: {BR}")  # Debugging output to check coordinates
    region = (TL[0], TL[1], BR[0], BR[1])

    for img in filepaths.honeyTradePaths:
        targetImage = cv2.imread(
            img, cv2.IMREAD_GRAYSCALE
        )  # Read the image in grayscale for better matching
        showGearShopCoords = locateTemplateOnScreen(region, targetImage)

        if showGearShopCoords is not None:
            autoit.click_absolute(showGearShopCoords[0], showGearShopCoords[1])
            autoit.click_window_center(
                False
            )  # Move mouse to the center of the screen to focus on the shop window
            sleep(2)  # Wait for the gear shop to open
            return True

    # If the gear shop options were not found, take a screenshot for debugging purposes
    screenshot = ImageGrab.grab(bbox=region)
    screenshotGray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    cv2.imwrite(f"debugScreenshotHONEYSHOPOPTIONS{timestamp}.png", screenshotGray)
    return False  # If the gear shop options were not found, return False    return False  # If the gear shop options were not found, return False
