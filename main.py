import threading
import window_actions as autoit
import importlib    
from datetime import datetime
from time import sleep

import Constants.constantsPositions as constants
import Constants.constantsFilepaths as filepaths
from actionQueue import ActionQueue
from buyEggs import buyEggShop
from buyGearShop import buyGearShop
from buyHoney import buyHoneyShop
from buySeedShop import buySeedShop
import sys
from threading import Event, Thread

from makeHoney import makeHoney
from moveTo import returnToGarden, moveToSeedShop, gotoSell
autoit.raw.auto_it_set_option("MouseCoordMode", 2)

def isFiveMinMark():
    return datetime.now().minute % 5 == 0

def focusGameWindow():
    '''
    Focuses the game window to ensure that the mouse clicks are registered correctly.
    '''
    autoit.raw.win_activate("Roblox")  # Activate the Roblox window
    sleep(0.5)  # Wait for the window to be activated
    autoit.click_window_center()

def resizeGameWindow():
    # Resize game window to smallest it can go with minmove
    autoit.raw.win_move("Roblox", 0, 0, 800, 600)  # Move
def toggleFollowMode():
    '''
    Toggles follow by pressing escape, tab, down arrow, x2 left arrow, and then escape again.
    '''
    autoit.send("{ESC}")
    sleep(0.5)  # Wait for the escape key to register
    autoit.send("{TAB}")
    sleep(0.4)  # Wait for the tab key to register
    autoit.send("{DOWN}")   
    sleep(0.1) # Wait for the down arrow key to register
    autoit.send("{LEFT}")
    sleep(0.2)  # Wait for the left arrow keys to register
    autoit.send("{LEFT}")
    sleep(0.2)  # Wait for the left arrow keys to register
    autoit.send("{ESC}")
    sleep(0.5)  # Wait for the escape key to register again

def zoomAlignment():
    autoit.wheel("up", 100)  # Scroll down to zoom in
    sleep(0.2)
    autoit.wheel("down", 8)  # Scroll down to zoom in
    sleep(0.2)

def cameraAlignment():
    autoit.click_window_center(False)
    sleep(0.2)
    autoit.mouse_down("right")
    sleep(0.2)  # Wait for the right click to register
    # move mouse to the center of the screen
    # move mouse down to align camera
    autoit.move(200, 600, 3)
    sleep(0.2)  # Wait for the mouse to move
    # right click release
    autoit.mouse_up("right")
    sleep(0.2)

def alignCamera():
    '''
    Aligns the camera by pressing the home key.
    This function is used to align the camera in the garden.
    '''

    # zoom all the way in
    zoomAlignment()
    toggleFollowMode()
    cameraAlignment()
    # right click hold down
    

    for i in range(12):
        gotoSell()
        moveToSeedShop()
    sleep(1)
    gotoSell()
    sleep(1)
    toggleFollowMode()
    returnToGarden()
    sleep(0.5)

def run_task_in_loop(interval_seconds, task_func):
    """
    Runs a task function in an infinite loop, sleeping for the interval.
    This function is meant to be the `target` of a `threading.Thread`.
    """
    while True:
        task_func()
        sleep(interval_seconds)

def clear_robux_popup():
    """
    Clears the Robux popup if it appears.
    This function is meant to be run in a separate thread.
    """
    autoit.send("{ESC}")
    sleep(0.1)
    autoit.send("{ESC}")
    sleep(0.5)

actionQueue = ActionQueue()
def main():
    focusGameWindow()
    resizeGameWindow()
    alignCamera()
    buy_honey_thread = threading.Thread(
    target=run_task_in_loop, 
    args=(1800, lambda: actionQueue.add(buyHoneyShop)),
    daemon=True
    )

    clear_thread = threading.Thread(
    target=run_task_in_loop, 
    args=(900, lambda: actionQueue.add(clear_robux_popup)),
    daemon=True
    )

    honey_thread = threading.Thread(
    target=run_task_in_loop, 
    args=(300, lambda: actionQueue.add(makeHoney)),
    daemon=True
    )

    gear_shop_thread = threading.Thread(
    target=run_task_in_loop, 
    args=(300, lambda: actionQueue.add(buyGearShop)),
    daemon=True
    )

    seed_shop_thread = threading.Thread(
    target=run_task_in_loop, 
    args=(300, lambda: actionQueue.add(buySeedShop)),
    daemon=True
    )

    egg_shop_thread = threading.Thread(
    target=run_task_in_loop, 
    args=(1800, lambda: actionQueue.add(buyEggShop)),
    daemon=True
    )

    print("Starting background tasks...")
    buy_honey_thread.start()
    clear_thread.start()
    honey_thread.start()
    gear_shop_thread.start()
    seed_shop_thread.start()
    egg_shop_thread.start()

    print("Background tasks started. The main program will now wait.")
    print("Press Ctrl+C to exit.")

    try:
        # This is a more efficient way to wait than a busy loop
        # The main thread will simply block here until an interrupt
        while True:
            sleep(3600) # Sleep for a long time
    except KeyboardInterrupt:
        print("\nShutdown signal received. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()