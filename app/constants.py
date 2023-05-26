from enum import Enum
from dataclasses import dataclass

# GPIO pins and PWM controller channels
CAMERA_GPIO = 0
INTAKE_SERVO_CHANNEL = 0  # PWM controller channel
FILTER_SERVO_CHANNEL = 1  # PWM controller channel
LED_CHANNEL = 2  # PWM controller channel

START_BUTTON_PIN = 10  # to be changed
STOP_BUTTON_PIN = 12  # to be changed

DC_MOTOR_EN_PIN = 25
DC_MOTOR_IN1_PIN = 24
DC_MOTOR_IN2_PIN = 23


# Servo angles
FILTER_SERVO_ANGLE_LEFT = 45
FILTER_SERVO_ANGLE_RIGHT = 135
# the difference between these two should be 90 degrees?

INTAKE_SERVO_ANGLE_ON = 60
INTAKE_SERVO_ANGLE_OFF = 0

# Coordinates to mark when intake servo to operate

# TODO: draw these lines on video
# x coordinate of where we consider intake servo should move to take the disc
INTAKE_AREA_X_LOW = 300
INTAKE_AREA_X_HIGH = 350

# y coordinate of line where we consider disc has moved onto belt
BELT_AREA_Y = 500


class DiscColours(str, Enum):
    WHITE = "white"
    BLACK = "black"


class Moves(str, Enum):
    LEFT = "left"
    RIGHT = "right"


COLOUR_FILTER_MAP = {DiscColours.WHITE: Moves.RIGHT, DiscColours.BLACK: Moves.LEFT}


@dataclass
class Instruction:
    time_added: int
    move: Moves


class RunStatus(int, Enum):
    LIVE = 1
    SIMULATION = 2
