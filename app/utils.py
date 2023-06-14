import time
from typing import List

import cv2
import numpy as np

from app.constants import DiscColours, Instruction, RunStatus, BELT_AREA_X_RIGHT, BELT_AREA_X_LEFT, BELT_AREA_Y_DOWN, BELT_AREA_Y_UP

SENSITIVITY = 50


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
        minRadius=85,
        maxRadius=115,
    )
    return circles


def rgb_to_color(r, g, b):
    print(f"r: {r}, g: {g}, b: {b}")
    if all(colour > 200 - SENSITIVITY for colour in [r, g, b]):
        return DiscColours.WHITE
    elif all(colour < 50 + SENSITIVITY for colour in [r, g, b]):
        return DiscColours.BLACK
    elif g > 190 - SENSITIVITY and r < 80 + SENSITIVITY and b < 80 + SENSITIVITY:
        return DiscColours.GREEN
    return None


def draw_lines(frame):
    cv2.line(frame, (BELT_AREA_X_LEFT, 1), (BELT_AREA_X_LEFT+1, 639), (0, 0, 255), thickness=2)
    cv2.line(frame, (BELT_AREA_X_RIGHT, 1), (BELT_AREA_X_RIGHT+1, 639), (0, 0, 255), thickness=2)
        
    cv2.line(frame, (1, BELT_AREA_Y_DOWN), (639, BELT_AREA_Y_DOWN), (0, 255, 0), thickness=2)
    cv2.line(frame, (1, BELT_AREA_Y_UP), (639, BELT_AREA_Y_UP), (255, 0, 0), thickness=2)


def detect_circles_current_frame(camera):
    frame = camera.current_frame
    if Environment().is_live:
        circles = get_circles_mask(frame)
        if circles is None:
            return []

        circles = np.round(circles[0, :]).astype(int)
        sanitized_circles = []
        # Draw detected circles
        for x, y, r in circles:
            if y > BELT_AREA_Y_DOWN or y < BELT_AREA_Y_UP or x > BELT_AREA_X_RIGHT + 100 or x < BELT_AREA_X_LEFT:
                continue

            if 1 < x < frame.shape[0]:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                cv2.circle(frame, (x, y - 50), 2, (0, 0, 255), 3)
                print(f"Colour point: x={x}, y={y-50}")
                colour = rgb_to_color(
                    frame[x, y - 50, 2],
                    frame[x, y - 50, 1],
                    frame[x, y - 50, 0],
                )
                if colour is None:
                    continue

                # print(f"Circle at {x}, {y} with colour: {colour}")
                sanitized_circles.append((x,y,r,colour))
        # draw_lines(frame)
        
        
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

    def add_instruction(self, time_added, disc):
        self.instructions = [
            Instruction(time_added=time_added, disc=disc)
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
