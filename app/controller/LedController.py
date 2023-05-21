import board
import busio
import adafruit_pca9685

from app.controller import BaseController

FULL_DUTY_CYCLE = 0xFFFF


class LedController(BaseController):
    def __init__(self, channel):
        i2c = busio.I2C(board.SCL, board.SDA)
        pca = adafruit_pca9685.PCA9685(i2c)
        super().__init__(pca, channel)
        self.led = pca.channels[channel]

    def turn_on(self):
        print(f"Turning on lamp on channel {self.channel}")
        self.led.duty_cycle = FULL_DUTY_CYCLE

    def turn_off(self):
        print(f"Turning off lamp on channel {self.channel}")
        self.led.duty_cycle = 0