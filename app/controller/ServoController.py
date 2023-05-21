from time import sleep
from adafruit_servokit import ServoKit

from app.controller import BaseController

ANGLE_TIME = 0.425 / 90


class ContinuousServoController(BaseController):
    def __init__(self, channel: int):
        kit = ServoKit(channels=16)
        super().__init__(kit, channel)
        self.servo = self.connector.continuous_servo[channel]

    def rotate_clockwise(self, angle: int):
        print(f"Rotating Servo {self.channel} - {angle} degrees clockwise")
        self.servo.throttle = -0.05
        sleep(ANGLE_TIME * angle)
        self.servo.throttle = 0
        return self

    def rotate_anticlockwise(self, angle:int):
        print(f"Rotating Servo {self.channel} - {angle} degrees clockwise")
        self.servo.throttle = 0.148
        sleep(ANGLE_TIME * angle)
        self.servo.throttle = 0
        return self


class StepperServoController(BaseController):

    def __init__(self, channel: int):
        kit = ServoKit(channels=16)
        super().__init__(kit, channel)
        self.servo = self.connector.servo[channel]

    def rotate_angle(self, angle: int):
        print(f"Rotating Servo {self.channel} - {angle} degrees clockwise")
        self.servo.angle = angle
        return self

