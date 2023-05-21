class BaseController:
    def __init__(self, connector, channel: int):
        self.connector = connector
        self.channel = channel

    def get_channel(self):
        return self.channel

    def __repr__(self):
        return f"Device {self.connector} on channel {self.channel}"

    def __str__(self):
        return f"Device {self.connector} on channel {self.channel}"