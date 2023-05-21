from abc import abstractmethod

import cv2
from time import sleep

from app.constants import CAMERA_GPIO
from app.controller import BaseController

RETRIES = 5


class CameraController(BaseController):
    def __init__(self):
        print(f"Connecting the camera on channel {CAMERA_GPIO}")
        camera = cv2.VideoCapture(CAMERA_GPIO)
        super().__init__(camera, CAMERA_GPIO)
        self.connector.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.connector.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.frame = None
        self.read_frame()

    def read_frame(self):
        retry_count = 1
        while True:
            ret, self.frame = self.connector.read()
            retry_count += 1
            if ret:
                break
            elif retry_count > RETRIES:
                print("Failed to read_frame from camera")
            sleep(0.05)

        return self.frame

    @property
    def current_frame(self):
        return self.frame

    def display_current_frame(self):
        # Display the frame using Matplotlib
        cv2.imshow("Camera feed", self.current_frame)

    @abstractmethod
    def draw_circle(self, image, x, y, radius, rgb, z):
        cv2.circle(image, (x, y), radius, rgb, z)

    def stop(self):
        print(f"Disconnecting the camera on channel {self.channel}")
        self.connector.release()
        cv2.destroyAllWindows()

