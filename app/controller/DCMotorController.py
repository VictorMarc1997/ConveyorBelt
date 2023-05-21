from app.controller import BaseController


# TO BE ADDED
class DCMotorController(BaseController):
    def __init__(self, connector, channel: int):
        super().__init__(connector, channel)

    def start(self):
        print(f"Starting the DC motor on pin {self.channel}")
        pass

    def stop(self):
        print(f"Stopping the DC motor on pin {self.channel}")
        pass
