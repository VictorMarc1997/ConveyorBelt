import time

from app.disc import DiscQueue
from app.utils import (
    detect_circles_current_frame,
    ProcessedDiscs,
    FilterServoInstructionsQueue,
)
from app.constants import (
    Moves,
    FILTER_SERVO_ANGLE_LEFT,
    FILTER_SERVO_ANGLE_RIGHT,
    INTAKE_SERVO_ANGLE_ON,
    INTAKE_SERVO_ANGLE_OFF,
)

DELAY_TO_REACH_FILTER = 3


class BeltService:
    def __init__(self):
        self.camera = None
        self.led = None
        self.filter_servo = None
        self.intake_servo = None
        self.belt_motor = None

        self.start_time = None

        self.disc_queue = DiscQueue()
        self.running = False
        self.filter_instructions = FilterServoInstructionsQueue()
        self.processed_discs = ProcessedDiscs()

    def set_camera(self, camera):
        self.camera = camera
        return self

    def set_led(self, led):
        self.led = led
        return self

    def set_filter_servo(self, filter_servo):
        self.filter_servo = filter_servo
        return self

    def set_intake_servo(self, intake_servo):
        self.intake_servo = intake_servo
        return self

    def set_belt_motor(self, belt_motor):
        self.belt_motor = belt_motor
        return self

    def start_belt(self):
        print("Starting belt")
        self.belt_motor.start()

    def stop_belt(self):
        print("Stopping belt")
        self.belt_motor.stop()

    def turn_on(self):
        self.led.turn_on()
        self.start_belt()
        self.running = True

    def turn_off(self):
        self.led.turn_off()
        self.stop_belt()
        self.running = False

    def run(self):
        self.turn_on()
        self._run()

    def move_intake_servo(self, active):
        if active:
            self.intake_servo.angle(INTAKE_SERVO_ANGLE_ON)
        else:
            self.intake_servo.angle(INTAKE_SERVO_ANGLE_OFF)

    def move_filter_servo(self):
        instruction = self.filter_instructions.get_instruction(DELAY_TO_REACH_FILTER)
        if instruction:
            if instruction.move == Moves.LEFT:
                print(
                    f"Sorting Disc <{self.disc_queue.get_most_right_disc()}> "
                    f"to colour black"
                )
                self.filter_servo.rotate_angle(FILTER_SERVO_ANGLE_LEFT)
            elif instruction.move == Moves.RIGHT:
                print(
                    f"Sorting Disc <{self.disc_queue.get_most_right_disc()}> "
                    f"to colour white"
                )
                self.filter_servo.rotate_angle(FILTER_SERVO_ANGLE_RIGHT)

    def _run(self):
        self.start_time = time.time()

        while self.running:
            circles = detect_circles_current_frame(self.camera)
            self.disc_queue.add_or_update_discs(circles)

            if self.disc_queue.check_disk_at_servo():
                print(f"Moving Disc <{self.disc_queue.get_most_right_disc()}> to belt")
                self.move_intake_servo(active=True)

            elif self.disc_queue.check_disk_moved_to_belt():
                self.move_intake_servo(active=False)
                move_time = time.time()
                self.filter_instructions.add_instruction(
                    move_time, self.disc_queue.get_most_right_disc().colour
                )

            self.move_filter_servo()

        self.turn_off()
