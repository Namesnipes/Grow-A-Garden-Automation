import Constants.constantsPositions as constants
import window_actions


def returnToGarden():
    """
    Returns the player to the garden by clicking the garden button, resetting the cycle.
    """

    window_actions.move(constants.gardenButtonPosX, constants.gardenButtonPosY, 3)
    window_actions.click("left")  # Click the garden button to return to the garden
    window_actions.click_window_center(
        False
    )  # Move mouse to the center of the screen to finish off nicely


def moveToSeedShop():
    """
    Moves the player to the seed shop.
    This function should be called before buying seeds.
    """

    window_actions.move(constants.seedsButtonPosX, constants.seedsButtonPosY, 3)
    window_actions.click("left")  # Click the seeds button to open the seed shop


def gotoSell():
    """
    Moves the player to the sell button in the garden.
    This function is used to sell items in the garden.
    """

    window_actions.move(constants.sellButtonPosX, constants.sellButtonPosY, 3)
    window_actions.click("left")  # Click the sell button to open the sell menu
    window_actions.click("left")  # Click the sell button to open the sell menu
