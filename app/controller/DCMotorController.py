from app.controller import BaseController
from app.utils import Environment

# COMMENT THESE LIBRARIES TO RUN SIMULATION
import RPi.GPIO as GPIO

PWM_ON = 33
PWM_OFF = 0


class DCMotorController(BaseController):
    env = Environment()

    def __init__(self, en, in1, in2):
        self.en = en
        self.in1 = in1
        self.in2 = in2
        self.motor_pwm = None

        if self.env.is_live:
            self.setup()

        super().__init__(self.motor_pwm, en)

        self.set_forward()

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setup(self.en, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        self.motor_pwm = GPIO.PWM(self.en, 100)
        self.motor_pwm.start(0)

    def set_forward(self):
        print("Setting DC Motor rotation to forward")
        if self.env.is_live:
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
        return self

    def set_backward(self):
        print("Setting DC Motor rotation to backward")
        if self.env.is_live:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
        return self

    def start(self):
        print(f"Starting the DC Motor on pin {self.channel}")
        if self.env.is_live:
            self.motor_pwm.ChangeDutyCycle(PWM_ON)

    def stop(self):
        print(f"Stopping the DC Motor on pin {self.channel}")
        if self.env.is_live:
            self.motor_pwm.ChangeDutyCycle(PWM_OFF)
