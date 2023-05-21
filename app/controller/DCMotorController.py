import RPi.GPIO as GPIO

from app.controller import BaseController


class DCMotorController(BaseController):
    def __init__(self, en, in1, in2):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(en, GPIO.OUT)
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        self.motor_pwm = GPIO.PWM(en, 100)
        self.motor_pwm.start(0)
        self.in1 = in1
        self.in2 = in2
        super().__init__(self.motor_pwm, en)

        self.set_forward()

    def set_forward(self):
        print("Setting DC Motor rotation to forward")
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        return self

    def set_backward(self):
        print("Setting DC Motor rotation to backward")
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        return self

    def start(self):
        print(f"Starting the DC Motor on pin {self.channel}")
        self.motor_pwm.ChangeDutyCycle(100)

    def stop(self):
        print(f"Stopping the DC Motor on pin {self.channel}")
        self.motor_pwm.ChangeDutyCycle(0)
