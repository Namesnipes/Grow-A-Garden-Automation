from time import sleep

import cv2

import Constants.constantsFilepaths as filepaths
import Constants.constantsPositions as constants
import window_actions as autoit
from locateTemplateOnScreen import locateTemplateOnScreen


def getMoneySymbol():
    """
    Detects the money symbol in the shop window to ensure that the player has enough money to buy items.
    Returns True if the money symbol is found, False otherwise.
    """

    region = (
        constants.shopWindowPosX1,
        constants.shopWindowY1,
        constants.shopWindowPosX2,
        constants.shopWindowY2,
    )
    moneySymbolImage = cv2.imread(filepaths.moneySymbolImagePath, cv2.IMREAD_GRAYSCALE)

    moneySymbolCoords = locateTemplateOnScreen(region, moneySymbolImage, grayscale=True)

    if moneySymbolCoords is not None:
        print(f"Money symbol found at coordinates: {moneySymbolCoords}")
        return moneySymbolCoords
    else:
        print("Money symbol not found.")
        return None


def buy(thingsToBuy, PriceCheck=getMoneySymbol):
    """
    Automatically buys the desired items from a given shop in the game.
    """

    toBuy = list(thingsToBuy)
    autoit.wheel("up", 100)  # Scroll up to the top of the shop

    while len(toBuy) > 0:
        updatedToBuy = list(
            toBuy
        )  # To prevent modifying the list while iterating over it
        found = False  #  Flag to determine if we need to scroll down to find more items

        for imagePath in toBuy:
            coords = None  # Initialize coords to None for each item
            tries = 0
            while coords is None:
                print(imagePath)
                targetImage = cv2.imread(
                    imagePath, cv2.IMREAD_GRAYSCALE
                )  # Read the image in grayscale for better matching
                # Defines the region of the shop window
                region = (
                    constants.shopWindowPosX1,
                    constants.shopWindowY1,
                    constants.shopWindowPosX2,
                    constants.shopWindowY2,
                )
                coords = locateTemplateOnScreen(region, targetImage)
                # repeat until coords not none
                if coords is None:
                    print(
                        f"Item not found: {imagePath}. Scrolling down..."
                    )  # Debugging output to see which item is not found
                    # debug save screenshot
                    autoit.wheel(
                        "down", 1
                    )  # Scroll down by one click to look at the next item in the shop
                    sleep(0.4)  # Wait for the scroll animation to finish
                    tries += 1
                    if (
                        tries > 10
                    ):  # If we have tried to find the item more than 10 times, break out of the loop
                        print(f"Item {imagePath} not found after 10 tries. Skipping...")
                        updatedToBuy.remove(imagePath)
                        break  # Break out of the while loop to move on to the next item

            if coords is not None:  # Found item in the shop
                print(
                    f"Found item: {imagePath} at coordinates: {coords}"
                )  # Debugging output to see where the item was found
                updatedToBuy.remove(
                    imagePath
                )  # Remove the item from the list after buying it so we don't look for it again

                autoit.click_absolute(coords[0], coords[1])
                sleep(0.5)  # Wait for the animation to finish
                moneySymbolCoords = PriceCheck()

                if (
                    moneySymbolCoords is not None
                ):  # Found the money symbol indicating that we can buy the item
                    autoit.click_absolute(moneySymbolCoords[0], moneySymbolCoords[1])
                    # TODO: Modify this so it's not hardcoded to click 25 times
                    # Some of those clicks won't register because we click so fast
                    for _ in range(25):
                        autoit.click("left")

        toBuy = list(updatedToBuy)
