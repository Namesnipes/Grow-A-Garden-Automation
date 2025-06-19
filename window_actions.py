import datetime
import functools
from time import sleep
import autoit
import cv2
import numpy as np
from PIL import ImageGrab

from Constants import constantsFilepaths
from locateTemplateOnScreen import locateTemplateOnScreen

ROBLOX_WINDOW_TITLE = "Roblox"
ROBLOX_WINDOW_HWID = autoit.win_get_handle(ROBLOX_WINDOW_TITLE)


def ensure_roblox_active(func):
    """
    A decorator to ensure the 'Roblox' window is active before executing the decorated function.
    Attempts to activate 'Roblox' if it's not currently active.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        is_active = autoit.win_active(ROBLOX_WINDOW_TITLE)

        if not is_active:
            print(
                f"Pre-check: Window '{ROBLOX_WINDOW_TITLE}' is NOT active for '{func.__name__}'."
            )
            return False  # Or raise a custom exception here

        print(f"Executing '{func.__name__}' for '{ROBLOX_WINDOW_TITLE}'...")
        return func(*args, **kwargs)  # Execute the original autoit function

    return wrapper


# --- Public API: Your Wrapped "Safe" Functions ---
@ensure_roblox_active
def click(*args, **kwargs):
    """
    Performs a mouse click ensuring Roblox is active.
    (Wrapped autoit.mouse_click)
    """
    return autoit.mouse_click(*args, **kwargs)


@ensure_roblox_active
def mouse_down(*args, **kwargs):
    """
    Presses a mouse button ensuring Roblox is active.
    (Wrapped autoit.mouse_down)
    """
    return autoit.mouse_down(*args, **kwargs)


@ensure_roblox_active
def mouse_up(*args, **kwargs):
    """
    Releases a mouse button ensuring Roblox is active.
    (Wrapped autoit.mouse_up)
    """
    return autoit.mouse_up(*args, **kwargs)


@ensure_roblox_active
def send(*args, **kwargs):
    """
    Sends keyboard input ensuring Roblox is active.
    (Wrapped autoit.send)
    """
    return autoit.send(*args, **kwargs)


@ensure_roblox_active
def move(*args, **kwargs):
    """
    Moves the mouse ensuring Roblox is active.
    (Wrapped autoit.mouse_move)
    """
    return autoit.mouse_move(*args, **kwargs)


@ensure_roblox_active
def wheel(*args, **kwargs):
    """
    Scrolls the mouse wheel ensuring Roblox is active.
    (Wrapped autoit.mouse_wheel)
    """
    return autoit.mouse_wheel(*args, **kwargs)


# --- Higher Level Functions ---


def click_window_center(mouse_click=True):
    """
    Clicks the center of the active roblox window.
    This function is used to ensure that the mouse is centered in the game window.
    """
    size = autoit.win_get_client_size("Roblox")
    if mouse_click:
        click("left", x=size[0] // 2, y=size[1] // 2)
    else:
        move(x=size[0] // 2, y=size[1] // 2)


def click_absolute(x, y):
    """
    Clicks at the absolute coordinates (x, y) on the screen.
    This function is used to click at specific coordinates on the screen.
    """
    autoit.auto_it_set_option("MouseCoordMode", 1)
    move(x, y)  # Move mouse to the clicked position for visual feedback
    click("left", x, y)
    autoit.auto_it_set_option("MouseCoordMode", 2)


# --- Highest Level Functions ---


def closeGui():
    """
    Closes the gear shop GUI by clicking the shop button twice.
    """

    region = (0, 0, 300, 600)
    XImage = cv2.imread(constantsFilepaths.shopButtonImagePath, cv2.IMREAD_GRAYSCALE)
    XButtonCoords = locateTemplateOnScreen(region, XImage)

    if XButtonCoords is not None:
        click_absolute(
            XButtonCoords[0], XButtonCoords[1]
        )  # Click the X button to close the gear shop
        sleep(0.2)
        click_absolute(XButtonCoords[0], XButtonCoords[1])
        click_window_center(False)
        return True

    else:
        print("Failed to close the gui. The shop button was not found.")
        # Take a screenshot for debugging purposes
        screenshot = ImageGrab.grab(bbox=region)
        screenshotGray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        cv2.imwrite(f"debugScreenshot{timestamp}.png", screenshotGray)
        return False


raw = autoit
