import numpy as np

def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def eye_aspect_ratio(eye):

    A = distance(eye[1], eye[5])
    B = distance(eye[2], eye[4])
    C = distance(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)
    return ear