from app.disc import Disc
from app.constants import BELT_AREA_X_LEFT, BELT_AREA_X_RIGHT


class DiscQueue:
    def __init__(self):
        self.discs = []

    def add_disc(self, disc: Disc):
        if len(self.discs) == 0 and disc.x < BELT_AREA_X_RIGHT:
            print(f"Adding new disc: {disc}")
            self.discs = [disc]

    def pop_disc(self):
        return self.discs.pop()
    
    def show_discs(self):
        print(f", ".join(str(disc) for disc in self.discs))

    def get_most_right_disc(self):
        return self.discs[0] if len(self.discs) > 0 else None

    def add_or_update_discs(self, circles):
        i = 0
        while i < len(self.discs):
            found = False
            i_c = 0
            while i_c < len(circles):
                circle_x, circle_y = circles[i_c][0], circles[i_c][1]
                if self.discs[i].check_circle_is_disk(*circles[i_c]):
                    self.discs[i].update_position(circle_x, circle_y)
                    circles.remove(circles[i_c])
                    found = True
                    break
                i_c += 1

            if not found:
                lost = self.discs[i].missed_frame()
                if lost:
                    return self.discs.pop(i)
            i += 1
        
        for circle in circles:
            self.add_disc(Disc(*circle))

        return

    def check_disk_ready_to_sort(self):
        last_disc = self.get_most_right_disc()
        ready = last_disc and BELT_AREA_X_RIGHT < last_disc.x
        if ready:
            self.pop_disc()
            return last_disc
