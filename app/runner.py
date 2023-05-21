from app.service import BeltService
from app.constants import LED_CHANNEL, INTAKE_SERVO_CHANNEL, FILTER_SERVO_CHANNEL, START_BUTTON_PIN, STOP_BUTTON_PIN, \
    DC_MOTOR_PIN
from app.controller import ButtonController, StepperServoController, CameraController, LedController, DCMotorController

if __name__ == "__main__":
    belt_motor = DCMotorController(None, DC_MOTOR_PIN)  # <-- change this

    camera = CameraController()
    led = LedController(LED_CHANNEL)
    intake_servo = StepperServoController(INTAKE_SERVO_CHANNEL)  # use ContinuousServoController if 360 servo
    filter_servo = StepperServoController(FILTER_SERVO_CHANNEL)

    start_button = ButtonController(START_BUTTON_PIN)
    stop_button = ButtonController(STOP_BUTTON_PIN)

    service = BeltService()\
        .set_camera(camera)\
        .set_led(led)\
        .set_belt_motor(belt_motor)\
        .set_intake_servo(intake_servo)\
        .set_filter_servo(filter_servo)
    start_button.set_event(service.turn_on)
    stop_button.set_event(service.turn_off)

    service.run()




