from enum import Enum
from dataclasses import dataclass
from app.disc import Disc

# GPIO pins and PWM controller channels
CAMERA_GPIO = 0
INTAKE_SERVO_CHANNEL = 0  # PWM controller channel
FILTER_SERVO_CHANNEL = 1  # PWM controller channel
LED_CHANNEL = 2  # PWM controller channel

START_BUTTON_PIN = 7
STOP_BUTTON_PIN = 9
VCC_PINS = [11, 1]

DC_MOTOR_EN_PIN = 16
DC_MOTOR_IN1_PIN = 20
DC_MOTOR_IN2_PIN = 21


# Servo angles
FILTER_SERVO_ANGLE_WHITE = 0
FILTER_SERVO_ANGLE_TRASH = 90
FILTER_SERVO_ANGLE_BLACK = 120
# the difference between these two should be 90 degrees?

INTAKE_SERVO_ANGLE_ON = 60
INTAKE_SERVO_ANGLE_OFF = 0

# Coordinates to mark when intake servo to operate

# x coordinate of line where we consider disc has moved onto belt
BELT_AREA_X_LEFT = 200
BELT_AREA_X_RIGHT = 250
BELT_AREA_Y_DOWN = 350
BELT_AREA_Y_UP = 200


class DiscColours(str, Enum):
    WHITE = "white"
    BLACK = "black"
    GREEN = "green"


class Moves(str, Enum):
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"


COLOUR_FILTER_MAP = {
    DiscColours.WHITE: Moves.RIGHT, 
    DiscColours.BLACK: Moves.LEFT,
    None: Moves.MIDDLE,
}


@dataclass
class Instruction:
    time_added: int
    disc: Disc


class RunStatus(int, Enum):
    LIVE = 1
    SIMULATION = 2
