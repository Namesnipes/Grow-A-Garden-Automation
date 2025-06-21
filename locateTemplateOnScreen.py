import cv2
import numpy as np

# from datetime import datetime # For debugging purposes
from PIL import ImageGrab

import Constants.constantsScreenshot as constants


def locateTemplateOnScreen(region, targetImage, grayscale=True):
    """
    Takes a partial screenshot of the current screen and checks if the target image is present.
    If the target image is found, it returns the center coordinates of the target image.
    If the target image is not found, it returns None.
    """

    screenshot = ImageGrab.grab(bbox=region)
    if grayscale:
        screenshot = cv2.cvtColor(
            np.array(screenshot), cv2.COLOR_BGR2GRAY
        )  # Convert to grayscale for better matching
    else:
        screenshot = np.array(screenshot)
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    # cv2.imwrite(f"debugScreenshot{timestamp}.png", screenshotGray)  # Save the screenshot for debugging purposes

    bestMatch = None
    bestMatchValue = -1
    bestScale = 1.0

    # Scale the target images to find the match with the most confidence, preventing false positives
    for scale in np.arange(
        constants.scaleRange[0], constants.scaleRange[1], constants.scaleStep
    ):
        targetImageScaled = cv2.resize(targetImage, None, fx=scale, fy=scale)
        if grayscale:
            result = cv2.matchTemplate(
                screenshot, targetImageScaled, cv2.TM_CCOEFF_NORMED
            )  # TM_CCOEFF_NORMED is the most commonly used equation for template matching
        else:
            result = cv2.matchTemplate(screenshot, targetImageScaled, cv2.TM_SQDIFF)
        maxVal, _, maxLoc = cv2.minMaxLoc(result)[
            1:
        ]  # maxVal is the maximum confidence of the result for any pixel, and maxLoc is the coordinates of said pixel
        # print(f"Scale: {scale}, Max Value: {maxVal}, Max Location: {maxLoc}")
        if maxVal >= constants.threshold and maxVal > bestMatchValue:
            bestMatch = maxLoc
            bestMatchValue = maxVal
            bestScale = scale

    if bestMatch is not None:
        # Center coords to point the mouse to a more accurate position
        centerX = int(bestMatch[0] + targetImage.shape[1] * bestScale / 2)
        centerY = int(bestMatch[1] + targetImage.shape[0] * bestScale / 2)
        return (
            centerX + region[0],
            centerY + region[1],
        )  # Adjust for the region offset
    else:
        return None


def getColorOnScreen(hex):
    """
    Find the first pixel that matches the given hex color on the screen.

    :param hex: The hex color to search for (e.g., '#FF5733').
    :return: True if a pixel was clicked, False otherwise.
    """
    # Convert hex to RGB
    hex = hex.lstrip("#")
    rgb = tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))

    # Take a screenshot of the entire screen
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)

    # Convert the screenshot to RGB format
    screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    # Find all pixels that match the target color
    matching_pixels = np.where(np.all(screenshot_rgb == rgb, axis=-1))

    if matching_pixels[0].size > 0:
        # Click the first matching pixel
        x, y = matching_pixels[1][0], matching_pixels[0][0]
        return [x, y]

    return None
    return None
