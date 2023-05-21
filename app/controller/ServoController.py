from time import sleep

from app.controller import BaseController
from app.utils import Environment

# COMMENT THESE LIBRARIES TO RUN SIMULATION
from adafruit_servokit import ServoKit

ANGLE_TIME = 0.425 / 90


class ContinuousServoController(BaseController):
    env = Environment()

    def __init__(self, channel: int):
        if self.env.is_live:
            kit = ServoKit(channels=16)
            super().__init__(kit, channel)
            self.servo = self.connector.continuous_servo[channel]
        else:
            super().__init__(None, channel)
            self.servo = None

    def rotate_clockwise(self, angle: int):
        print(f"Rotating Servo {self.channel} - {angle} degrees clockwise")
        if self.env.is_live:
            self.servo.throttle = -0.05
            sleep(ANGLE_TIME * angle)
            self.servo.throttle = 0
        return self

    def rotate_anticlockwise(self, angle: int):
        print(f"Rotating Servo {self.channel} - {angle} degrees clockwise")
        if self.env.is_live:
            self.servo.throttle = 0.148
            sleep(ANGLE_TIME * angle)
            self.servo.throttle = 0
        return self


class StepperServoController(BaseController):
    env = Environment()

    def __init__(self, channel: int):
        if self.env.is_live:
            kit = ServoKit(channels=16)
            super().__init__(kit, channel)
            self.servo = self.connector.servo[channel]
        else:
            super().__init__(None, channel)
            self.servo = None

    def rotate_angle(self, angle: int):
        print(f"Rotating Servo {self.channel} - {angle} degrees clockwise")
        if self.env.is_live:
            self.servo.angle = angle
        return self
