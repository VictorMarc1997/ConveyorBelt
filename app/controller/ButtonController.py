from app.controller import BaseController
import RPi.GPIO as GPIO  # imported from python-rpi.gpio


class ButtonController(BaseController):
    def __init__(self, pin):
        super().__init__(None, pin)
        self.pin = pin
        # Import Raspberry Pi GPIO library
        GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering / Maybe disable this
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def set_event(self, callback_fn):
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=callback_fn)  # Setup event on pin 10 rising edge

