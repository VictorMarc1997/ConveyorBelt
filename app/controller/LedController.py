from app.controller import BaseController
from app.utils import Environment

# COMMENT THESE LIBRARIES TO RUN SIMULATION
import board
import busio
import adafruit_pca9685

FULL_DUTY_CYCLE = 13000


class LedController(BaseController):
    env = Environment()

    def __init__(self, channel):
        if self.env.is_live:
            i2c = busio.I2C(board.SCL, board.SDA)
            pca = adafruit_pca9685.PCA9685(i2c)
            super().__init__(pca, channel)
            self.led = pca.channels[channel]
        else:
            super().__init__(None, channel)
            self.led = None

    def turn_on(self):
        print(f"Turning on lamp on channel {self.channel}")
        if self.env.is_live:
            self.led.duty_cycle = FULL_DUTY_CYCLE

    def turn_off(self):
        print(f"Turning off lamp on channel {self.channel}")
        if self.env.is_live:
            self.led.duty_cycle = 0
