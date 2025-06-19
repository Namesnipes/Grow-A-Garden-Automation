import datetime
import functools
from time import sleep
import autoit
from autoit import AutoItError
import cv2
import numpy as np
from PIL import ImageGrab
import logging

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
            logging.info(
                f"Pre-check: Window '{ROBLOX_WINDOW_TITLE}' is NOT active for '{func.__name__}'."
            )
            quit()
            return False  # Or raise a custom exception here

        logging.debug(f"Executing '{func.__name__}' for '{ROBLOX_WINDOW_TITLE}'...")
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

from ctypes.wintypes import BOOL, HWND, POINT
from ctypes import byref

# What you NEED to add:
from ctypes import WinDLL, POINTER # <--- These two imports

# Load user32.dll for standard Windows API functions
User32 = WinDLL('user32') # <--- This line loads a system DLL, not a package

# Define the ScreenToClient function signature
# BOOL WINAPI ScreenToClient(HWND hWnd, LPPOINT lpPoint);
User32.ScreenToClient.restype = BOOL
User32.ScreenToClient.argtypes = [HWND, POINTER(POINT)] # <--- This defines how to call the function

# ... (your existing functions) ...

# Your new function
def convert_absolute_to_client_coords(abs_x, abs_y, handle=ROBLOX_WINDOW_HWID):
    """
    Converts absolute screen coordinates to client coordinates relative to a window.

    :param handle: The handle (HWND) of the window.
    :param abs_x: The absolute X coordinate on the screen.
    :param abs_y: The absolute Y coordinate on the screen.
    :return: A tuple (client_x, client_y) representing the coordinates
             relative to the window's client area.
    :raises AutoItError: If the conversion fails (e.g., invalid window handle).
    """
    # Create a POINT structure and set its initial values to the absolute coordinates
    point = POINT(abs_x, abs_y)

    # Call the ScreenToClient function. It modifies the 'point' structure in-place.
    ret = User32.ScreenToClient(HWND(handle), byref(point))

    if not ret:
        # ScreenToClient returns FALSE (0) on failure
        # GetLastError might provide more specific error details if needed
        # import ctypes
        # error_code = ctypes.GetLastError()
        # error_message = ctypes.FormatError(error_code)
        raise AutoItError(f"Failed to convert absolute coordinates to client "
                          f"for window handle {handle}. Absolute coords: ({abs_x}, {abs_y}).")

    return point.x, point.y


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
