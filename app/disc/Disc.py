from math import sqrt

from app.constants import DiscColours
from app.utils import ProcessedDiscs

DISK_DIAMETER = 20  # pixels, needs to be tested
DISK_RADIUS_ERROR_THRESHOLD = 5  # pixels of accepted error in disk radius

MISSED_FRAMES_THRESHOLD = 5


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
        return f"Disc #{self.id} - colour: {self.colour}"

    def __str__(self):
        return f"Disc #{self.id} - colour: {self.colour}"

    def set_lost(self):
        print(f"Lost detection for Disc #{self.id}")
        self.tracked = False

    def missed_frame(self):
        if self.missed_frames > MISSED_FRAMES_THRESHOLD:
            self.set_lost()
        else:
            self.missed_frames += 1

    def check_circle_is_disk(self, x, y, radius, colour):
        dist_from_last_point = sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

        return (
            self.tracked
            and colour == self.colour
            and abs(radius - self.radius) <= DISK_RADIUS_ERROR_THRESHOLD
            and dist_from_last_point <= DISK_DIAMETER // 2
        )

    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.missed_frames = 0
