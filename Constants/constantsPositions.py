import pyautogui

'''
Feel free to modify the relative positions of the buttons based on your screen resolution, if you like.
The hope is that with relative positions, the code will work on any screen resolution.
'''

screenWidth, screenHeight = pyautogui.size()

# Relative positions for buttons that do not change position
seedsButtonRelativeX = 249 / screenWidth
seedsButtonRelativeY = 89 / screenHeight
seedsButtonPosX, seedsButtonPosY = int(screenWidth * seedsButtonRelativeX), int(screenHeight * seedsButtonRelativeY)

gardenButtonRelativeX = 396 / screenWidth
gardenButtonRelativeY = 90 / screenHeight
gardenButtonPosX, gardenButtonPosY = int(screenWidth * gardenButtonRelativeX), int(screenHeight * gardenButtonRelativeY)

sellButtonRelativeX = 551 / screenWidth
sellButtonRelativeY = 90 / screenHeight
sellButtonPosX, sellButtonPosY = int(screenWidth * sellButtonRelativeX), int(screenHeight * sellButtonRelativeY)

# Center of the screen, which is used to interact with the store
middleX, middleY = screenWidth // 2, screenHeight // 2

# Number of scrolls to perform to reach the bottom of the shops
# These values may need to be adjusted based on how far your scroll wheel scrolls
numScrollsGearShop = 15
numScrollsSeedsShop = 7

# Dimensions of the shop window, which will be used to take a screenshot and detect items
# Top left corner of the shop window
shopWindowX1 = 193 / screenWidth
shopWindowY1 = 145 / screenHeight
# Bottom right corner of the shop window
shopWindowX2 = 606 / screenWidth
shopWindowY2 = 510 / screenHeight
# Convert to relative positions
shopWindowPosX1, shopWindowY1 = int(screenWidth * shopWindowX1), int(screenHeight * shopWindowY1)
shopWindowPosX2, shopWindowY2 = int(screenWidth * shopWindowX2), int(screenHeight * shopWindowY2)

# The keybind to hold the recall wrench, which teleports the player to the gear shop
recallWrenchKeybind = "2"  # Change this to the keybind you use for the recall wrench

# Dimensions of the gear shop options menu, which will be used to detect the option that opens the gear shop
# Top left corner of the gear shop options menu 470, 271
gearShopOptionsX1 = 470 / screenWidth
gearShopOptionsY1 = 271 / screenHeight
# Bottom right corner of the gear shop options menu 767, 345
gearShopOptionsX2 = 767 / screenWidth
gearShopOptionsY2 = 345 / screenHeight
# Convert to relative positions
gearShopOptionsPosX1, gearShopOptionsY1 = int(screenWidth * gearShopOptionsX1), int(screenHeight * gearShopOptionsY1)
gearShopOptionsPosX2, gearShopOptionsY2 = int(screenWidth * gearShopOptionsX2), int(screenHeight * gearShopOptionsY2)