from app.disc import Disc
from app.constants import INTAKE_AREA_X_LOW, INTAKE_AREA_X_HIGH, BELT_AREA_Y


class DiscQueue:
    def __init__(self):
        self.discs = []

    def add_disc(self, disc: Disc):
        self.discs = [disc] + self.discs

    def pop_disc(self):
        return self.discs.pop()

    def valid_new_disk(self, x):
        # TODO: check if x axis goes up to right or to left
        return all(disc.x > x for disc in self.discs)

    def add_or_update_discs(self, circles):
        for disc in self.discs:
            found = False
            for circle in circles:
                circle_x, circle_y = circle[0], circle[1]
                if disc.check_circle_is_disk(**circle):
                    disc.update_position(circle_x, circle_y)
                    found = True
                    break
                if self.valid_new_disk(circle_x):
                    found = True
                    self.add_disc(Disc(**circles))
            if not found:
                disc.missed_frame()

        return self

    def check_disk_at_servo(self):
        last_disc = self.discs[-1]
        return (
            last_disc.id % 3 == 1
            and INTAKE_AREA_X_LOW < last_disc.x < INTAKE_AREA_X_HIGH
        )

    def check_disk_moved_to_belt(self):
        return BELT_AREA_Y > self.discs[-1].y
