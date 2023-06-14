from math import sqrt

from app.constants import DiscColours
from app.utils import ProcessedDiscs

DISK_DIAMETER = 200  # pixels, needs to be tested
DISK_RADIUS_ERROR_THRESHOLD = 40  # pixels of accepted error in disk radius

MISSED_FRAMES_THRESHOLD = 4 # to be tested


class Disc:
    def __init__(self, x, y, radius, colour: DiscColours):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.tracked = True
        self.missed_frames = 0

        self.id = ProcessedDiscs().add(colour).get_count_all()

    def __repr__(self):
        return f"Disc #{self.id} - colour: {self.colour} - x: {self.x}, y:{self.y}"

    def __str__(self):
        return f"Disc #{self.id} - colour: {self.colour} - x: {self.x}, y:{self.y}"

    def set_lost(self):
        print(f"Lost detection for Disc #{self.id}")
        self.tracked = False

    def missed_frame(self):
        print(f"{str(self)} missed frame {self.missed_frames}")
        if self.missed_frames > MISSED_FRAMES_THRESHOLD:
            self.set_lost()
            return True
        else:
            self.missed_frames += 1

    def check_circle_is_disk(self, x: int, y: int, radius: int, colour: DiscColours):
        # dist_from_last_point = sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

        return (
            self.tracked
            and colour == self.colour
            and x > self.x
            and abs(radius - self.radius) <= DISK_RADIUS_ERROR_THRESHOLD
        )

    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.missed_frames = 0
