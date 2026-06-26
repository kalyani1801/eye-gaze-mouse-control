import time


class FatigueDetector:

    def __init__(self):

        self.closed_start = None


    def detect(self, ear):

        if ear < 0.18:

            if self.closed_start is None:
                self.closed_start = time.time()

            if time.time() - self.closed_start > 3:
                return True

        else:
            self.closed_start = None

        return False