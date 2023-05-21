import cv2
import numpy as np

from constants import DiscColours
from controller.CameraController import CameraController

WHITE_SENSITIVITY = 30
BLACK_SENSITIVITY = 50


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


def get_circles_mask(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect circles using Hough transform
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                               param1=50, param2=30, minRadius=10, maxRadius=100)
    return circles


def rgb_to_color(r, g, b):

    if all(colour > 255 - WHITE_SENSITIVITY for colour in [r, g, b]):
        return DiscColours.WHITE
    elif all(colour < BLACK_SENSITIVITY for colour in [r, g, b]):
        return DiscColours.BLACK
    return None


def detect_circles_current_frame(camera: CameraController):
    circles = get_circles_mask(camera.current_frame)
    if circles is None:
        return None

    circles = np.round(circles[0, :]).astype(int)
    sanitized_circles = []
    # Draw detected circles
    for (x, y, r) in circles:
        camera.draw_circle(camera.current_frame, x, y, r, (0, 255, 0), 2)
        camera.draw_circle(camera.current_frame, x, y, 2, (0, 0, 255), 3)
        sanitized_circles.append((x, y, r, rgb_to_color(
            camera.current_frame[x, y, 2],
            camera.current_frame[x, y, 1],
            camera.current_frame[x, y, 0]
        )))
    return sanitized_circles
