import time
from enum import Enum
from dataclasses import dataclass
from typing import List

from app.utils import singleton

CAMERA_GPIO = 0
INTAKE_SERVO_CHANNEL = 0  # PWM controller channel
FILTER_SERVO_CHANNEL = 1  # PWM controller channel
LED_CHANNEL = 2  # PWM controller channel
START_BUTTON_PIN = 10  # to be changed
STOP_BUTTON_PIN = 12  # to be changed
DC_MOTOR_PIN = 16  # wrong?

FILTER_SERVO_ANGLE_LEFT = 45
FILTER_SERVO_ANGLE_RIGHT = 135  # the difference between these two is 90 degrees?

INTAKE_SERVO_ANGLE_ON = 60
INTAKE_SERVO_ANGLE_OFF = 0

INTAKE_AREA_X_LOW = 300  # x coordinate of where we consider intake servo should move to take the disc
INTAKE_AREA_X_HIGH = 350

BELT_AREA_Y = 500  # y coordinate of line where we consider disc has moved onto belt


class DiscColours(str, Enum):
    WHITE = "white"
    BLACK = "black"


class Moves(str, Enum):
    LEFT = "left"
    RIGHT = "right"


COLOUR_FILTER_MAP = {
    DiscColours.WHITE: Moves.RIGHT,
    DiscColours.BLACK: Moves.LEFT
}


@dataclass
class Instruction:
    time_added: int
    move: Moves


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
        self.instructions = [Instruction(time_added=time_added, move=COLOUR_FILTER_MAP[colour])] + self.instructions

    def get_instruction(self, delay):
        now = time.time()
        if now - self.instructions[-1].time_added > delay:
            return self.instructions.pop()
        return None
