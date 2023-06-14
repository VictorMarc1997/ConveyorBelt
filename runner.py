from app.service import BeltService
from app.constants import (
    LED_CHANNEL,
    INTAKE_SERVO_CHANNEL,
    FILTER_SERVO_CHANNEL,
    START_BUTTON_PIN,
    STOP_BUTTON_PIN,
    DC_MOTOR_EN_PIN,
    DC_MOTOR_IN1_PIN,
    DC_MOTOR_IN2_PIN,
    VCC_PINS,
)
from app.controller import (
    ButtonController,
    StepperServoController,
    ContinuousServoController,
    CameraController,
    LedController,
    DCMotorController,
)

from argparse import ArgumentParser

import RPi.GPIO as GPIO

from app.utils import Environment

parser = ArgumentParser(
    description="Program to control a conveyor belt for sorting discs"
)

parser.add_argument(
    "--simulate", action="store_true", help="Flag to simulate the run of conveyor"
)

def setup_pins():
    GPIO.setmode(GPIO.BCM)
    for pin in VCC_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

if __name__ == "__main__":
    setup_pins()
    args = parser.parse_args()


    if not args.simulate:
        Environment().set_live()

    belt_motor = DCMotorController(DC_MOTOR_EN_PIN, DC_MOTOR_IN1_PIN, DC_MOTOR_IN2_PIN)
    camera = CameraController()
    led = LedController(LED_CHANNEL)
    intake_servo = StepperServoController(INTAKE_SERVO_CHANNEL)
    filter_servo = ContinuousServoController(FILTER_SERVO_CHANNEL, intake_servo.connector)

    start_button = ButtonController(START_BUTTON_PIN)
    stop_button = ButtonController(STOP_BUTTON_PIN)

    service = BeltService()
        
    service \
        .set_camera(camera) \
        .set_led(led) \
        .set_belt_motor(belt_motor) \
        .set_intake_servo(intake_servo) \
        .set_filter_servo(filter_servo) \
        .set_start_button(start_button) \
        .set_stop_button(stop_button)

    service.run()
        

