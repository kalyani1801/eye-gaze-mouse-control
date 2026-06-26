import time
from utils import eye_aspect_ratio


class BlinkDetector:

    def __init__(self):

        self.EAR_THRESHOLD = 0.21
        self.blink_start = None
        self.last_blink = 0


    def detect(self, left_eye, right_eye):

        ear_left = eye_aspect_ratio(left_eye)
        ear_right = eye_aspect_ratio(right_eye)

        ear = (ear_left + ear_right) / 2

        if ear < self.EAR_THRESHOLD:

            if self.blink_start is None:
                self.blink_start = time.time()

        else:

            if self.blink_start is not None:

                duration = time.time() - self.blink_start
                self.blink_start = None

                if duration > 1:
                    return "RIGHT_CLICK"

                if time.time() - self.last_blink < 0.5:
                    self.last_blink = time.time()
                    return "DOUBLE_CLICK"

                self.last_blink = time.time()
                return "LEFT_CLICK"

        return None