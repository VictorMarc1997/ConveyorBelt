import time

from app.disc import DiscQueue
from app.utils import (
    detect_circles_current_frame,
    ProcessedDiscs,
    FilterServoInstructionsQueue,
)
from app.constants import (
    DiscColours,
    INTAKE_SERVO_ANGLE_ON,
    INTAKE_SERVO_ANGLE_OFF,
)

DELAY_TO_REACH_FILTER = 3.5  # seconds
INTAKE_TIME_TRESHOLD = 7 # seconds out of 10 seconds. For example 7 means it will intake every 10 seconds for 3 seconds between  7 and 10


class BeltService:
    running: bool
    DEFAULT_ON = 1

    def __init__(self):
        self.camera = None
        self.led = None
        self.filter_servo = None
        self.intake_servo = None
        self.belt_motor = None
        self.start_button = None
        self.stop_button = None

        self.start_time = None

        self.disc_queue = DiscQueue()
        self.running = False
        self.intake_servo_on = False
        self.filter_white = True
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
    
    def set_start_button(self, start_button):
        self.start_button = start_button
        return self
    
    def set_stop_button(self, stop_button):
        self.stop_button = stop_button
        return self
    
    def start_belt(self):
        print("Starting belt")
        self.belt_motor.start()

    def stop_belt(self):
        print("Stopping belt")
        self.belt_motor.stop()

    def turn_on(self):
        print(40 * "*")
        print("Turning ON")
        self.led.turn_on()
        self.start_belt()
        self.running = True

    def turn_off(self):
        print(40 * "*")
        print("Turning OFF")
        self.led.turn_off()
        self.stop_belt()
        self.running = False

    def move_intake_servo(self, active):
        if active:
            self.intake_servo_on = True
            self.intake_servo.rotate_angle(INTAKE_SERVO_ANGLE_ON)
        else:
            self.intake_servo_on = False
            self.intake_servo.rotate_angle(INTAKE_SERVO_ANGLE_OFF)

    def move_filter_servo(self):
        instruction = self.filter_instructions.get_instruction(DELAY_TO_REACH_FILTER)
        if instruction:
            if instruction.disc.colour == DiscColours.BLACK and self.filter_white:
                print(
                    f"Sorting Disc <{instruction.disc}> "
                    f"to colour black"
                )
                self.filter_servo.rotate_clockwise(180)
                self.filter_white = False
            elif instruction.disc.colour == DiscColours.WHITE and not self.filter_white:
                print(
                    f"Sorting Disc <{instruction.disc}> "
                    f"to colour white"
                )
                self.filter_servo.rotate_anticlockwise(180)
                self.filter_white = True

            '''elif instruction.move == Moves.MIDDLE:
                print(
                    f"Found Trash, not sorting"
                )
                self.filter_servo.rotate_angle(FILTER_SERVO_ANGLE_TRASH)'''
    
    def run(self):
        self.start_time = time.time()
        
        while True:
            if self.running:
                # get circles from camera
                self.camera.read_frame()
                circles = detect_circles_current_frame(self.camera)
                # print(f"Circles are: {circles}")
                self.camera.display_current_frame()
                
                # update Discs with the circles
                disc = self.disc_queue.add_or_update_discs(circles)
                # self.disc_queue.show_discs()

                current_time = time.time()
                time_passed = current_time - self.start_time
                if time_passed % 10 > INTAKE_TIME_TRESHOLD and not self.intake_servo_on:
                    self.move_intake_servo(active=True)
                elif time_passed % 10 <= INTAKE_TIME_TRESHOLD and self.intake_servo_on:
                    self.move_intake_servo(active=False)
                
                disc = self.disc_queue.check_disk_ready_to_sort() if disc is None else disc
                if disc:
                    print(f"Preparing disc {disc} to sort")
                    self.filter_instructions.add_instruction(
                        current_time, disc
                    )

                self.move_filter_servo()

                if self.stop_button.is_pressed():
                    self.turn_off()
            elif self.start_button.is_pressed():
                self.turn_on()
