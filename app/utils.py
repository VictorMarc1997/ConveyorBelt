import time
from typing import List

import cv2
import numpy as np

from app.constants import DiscColours, Instruction, COLOUR_FILTER_MAP, RunStatus

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
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=50,
        param2=30,
        minRadius=10,
        maxRadius=100,
    )
    return circles


def rgb_to_color(r, g, b):
    if all(colour > 255 - WHITE_SENSITIVITY for colour in [r, g, b]):
        return DiscColours.WHITE
    elif all(colour < BLACK_SENSITIVITY for colour in [r, g, b]):
        return DiscColours.BLACK
    return None


def detect_circles_current_frame(camera):
    if Environment().is_live:
        circles = get_circles_mask(camera.current_frame)
        if circles is None:
            return None

        circles = np.round(circles[0, :]).astype(int)
        sanitized_circles = []
        # Draw detected circles
        for x, y, r in circles:
            camera.draw_circle(camera.current_frame, x, y, r, (0, 255, 0), 2)
            camera.draw_circle(camera.current_frame, x, y, 2, (0, 0, 255), 3)
            sanitized_circles.append(
                (
                    x,
                    y,
                    r,
                    rgb_to_color(
                        camera.current_frame[x, y, 2],
                        camera.current_frame[x, y, 1],
                        camera.current_frame[x, y, 0],
                    ),
                )
            )
        return sanitized_circles
    else:
        return []


@singleton
class AllDiscs:
    count: int

    def __init__(self):
        self.count = 0

    def add(self):
        self.count += 1

    def reset(self):
        self.count = 0

    def get_count(self):
        return self.count


@singleton
class ProcessedDiscs:
    count: int
    white: int
    black: int

    def __init__(self):
        self.count = 0
        self.white = 0
        self.black = 0

    def add(self, colour: DiscColours):
        self.count += 1
        if colour == DiscColours.BLACK:
            self.black += 1
        elif colour == DiscColours.WHITE:
            self.white += 1
        return self

    def reset(self):
        self.count = 0
        self.white = 0
        self.black = 0
        return self

    def get_count_all(self):
        return self.count

    def get_count_white(self):
        return self.white

    def get_count_black(self):
        return self.black


@singleton
class FilterServoInstructionsQueue:
    instructions: List[Instruction]

    def __init__(self):
        self.instructions = []

    def add_instruction(self, time_added, colour):
        self.instructions = [
            Instruction(time_added=time_added, move=COLOUR_FILTER_MAP[colour])
        ] + self.instructions

    def get_instruction(self, delay):
        now = time.time()
        if self.instructions and now - self.instructions[-1].time_added > delay:
            return self.instructions.pop()
        return None


@singleton
class Environment:
    env: int

    def __init__(self):
        self.env = RunStatus.SIMULATION

    def set_simulation(self):
        self.env = RunStatus.SIMULATION

    def set_live(self):
        self.env = RunStatus.LIVE

    @property
    def is_simulation(self):
        return self.env == RunStatus.SIMULATION

    @property
    def is_live(self):
        return self.env == RunStatus.LIVE
