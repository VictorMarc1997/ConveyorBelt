from app.controller import BaseController

from app.utils import Environment

# COMMENT THESE LIBRARIES TO RUN SIMULATION
import RPi.GPIO as GPIO  # imported from python-rpi.gpio


class ButtonController(BaseController):
    env = Environment()

    def __init__(self, pin):
        super().__init__(None, pin)
        self.pin = pin
        if self.env.is_live:
            self.setup()

    def setup(self):
        GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering / Maybe disable this
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def set_event(self, callback_fn):
        if self.env.is_live:
            GPIO.add_event_detect(
                self.pin, GPIO.RISING, callback=callback_fn
            )  # Setup event on pin 10 rising edge
