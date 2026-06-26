import cv2
import mediapipe as mp
import numpy as np


class EyeTracker:

    def __init__(self):

        self.mp_face = mp.solutions.face_mesh

        self.face_mesh = self.mp_face.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1
        )

        self.LEFT_EYE = [33,160,158,133,153,144]
        self.RIGHT_EYE = [362,385,387,263,373,380]

        self.LEFT_IRIS = [474,475,476,477]
        self.RIGHT_IRIS = [469,470,471,472]


    def get_landmarks(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return None

        mesh = results.multi_face_landmarks[0]

        h, w = frame.shape[:2]

        points = []

        for lm in mesh.landmark:

            x = int(lm.x * w)
            y = int(lm.y * h)

            points.append((x, y))

        return points


    def extract_eyes(self, points):

        left_eye = [points[i] for i in self.LEFT_EYE]
        right_eye = [points[i] for i in self.RIGHT_EYE]

        left_iris = [points[i] for i in self.LEFT_IRIS]
        right_iris = [points[i] for i in self.RIGHT_IRIS]

        return left_eye, right_eye, left_iris, right_iris


    def iris_center(self, iris):

        iris = np.array(iris)

        center = np.mean(iris, axis=0)

        return center


    def gaze_direction(self, eye, iris):

        eye = np.array(eye)

        min_x = np.min(eye[:,0])
        max_x = np.max(eye[:,0])

        min_y = np.min(eye[:,1])
        max_y = np.max(eye[:,1])

        eye_center_x = (min_x + max_x) / 2
        eye_center_y = (min_y + max_y) / 2

        iris_center = self.iris_center(iris)

        dx = iris_center[0] - eye_center_x
        dy = iris_center[1] - eye_center_y

        threshold = 5

        direction = "CENTER"

        if dx > threshold:
            direction = "RIGHT"

        elif dx < -threshold:
            direction = "LEFT"

        elif dy > threshold:
            direction = "DOWN"

        elif dy < -threshold:
            direction = "UP"

        return direction