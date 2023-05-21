from app.service import BeltService
from app.constants import (
    LED_CHANNEL,
    INTAKE_SERVO_CHANNEL,
    FILTER_SERVO_CHANNEL,
    START_BUTTON_PIN,
    STOP_BUTTON_PIN,
    DC_MOTOR_EN_PIN,
    DC_MOTOR_IN1_PIN,
    DC_MOTOR_IN2_PIN,
)
from app.controller import (
    ButtonController,
    StepperServoController,
    CameraController,
    LedController,
    DCMotorController,
)


def create_belt_service() -> BeltService:
    belt_motor = DCMotorController(DC_MOTOR_EN_PIN, DC_MOTOR_IN1_PIN, DC_MOTOR_IN2_PIN)

    camera = CameraController()
    led = LedController(LED_CHANNEL)
    intake_servo = StepperServoController(INTAKE_SERVO_CHANNEL)
    filter_servo = StepperServoController(FILTER_SERVO_CHANNEL)

    start_button = ButtonController(START_BUTTON_PIN)
    stop_button = ButtonController(STOP_BUTTON_PIN)

    service = (
        BeltService()
        .set_camera(camera)
        .set_led(led)
        .set_belt_motor(belt_motor)
        .set_intake_servo(intake_servo)
        .set_filter_servo(filter_servo)
    )
    start_button.set_event(service.turn_on)
    stop_button.set_event(service.turn_off)

    return service
