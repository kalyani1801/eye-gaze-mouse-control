'''import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import os
import time

pyautogui.FAILSAFE = False

# Initialize mediapipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Webcam
cam = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size()

blink_start = None
last_blink = 0
blink_count = 0

gesture = []

while True:

    ret, frame = cam.read()

    if not ret:
        break

    frame = cv2.flip(frame,1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    output = face_mesh.process(rgb)

    frame_h, frame_w, _ = frame.shape

    if output.multi_face_landmarks:

        landmarks = output.multi_face_landmarks[0].landmark

        # RIGHT IRIS landmark
        iris = landmarks[474]

        iris_x = int(iris.x * frame_w)
        iris_y = int(iris.y * frame_h)

        cv2.circle(frame,(iris_x,iris_y),5,(0,255,0),-1)

        # map eye position to screen
        screen_x = np.interp(iris_x,[100,frame_w-100],[0,screen_w])
        screen_y = np.interp(iris_y,[100,frame_h-100],[0,screen_h])

        pyautogui.moveTo(screen_x,screen_y)

        # blink detection
        top = landmarks[159]
        bottom = landmarks[145]

        top_y = int(top.y * frame_h)
        bottom_y = int(bottom.y * frame_h)

        cv2.circle(frame,(int(top.x*frame_w),top_y),3,(255,0,0),-1)
        cv2.circle(frame,(int(bottom.x*frame_w),bottom_y),3,(255,0,0),-1)

        if abs(top_y - bottom_y) < 5:

            if blink_start is None:
                blink_start = time.time()

        else:

            if blink_start is not None:

                duration = time.time() - blink_start
                blink_start = None

                if duration > 1:
                    pyautogui.rightClick()
                    cv2.putText(frame,"RIGHT CLICK",(50,100),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                elif time.time() - last_blink < 0.5:
                    pyautogui.doubleClick()
                    cv2.putText(frame,"DOUBLE CLICK",(50,100),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                else:
                    pyautogui.click()
                    cv2.putText(frame,"LEFT CLICK",(50,100),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                last_blink = time.time()

    cv2.imshow("Eye Gaze Mouse Control",frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()'''
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import os
import time

pyautogui.FAILSAFE = False

# -----------------------------
# CUSTOM LOCK GESTURE
# change this number if needed
# -----------------------------
LOCK_BLINK_COUNT = 5

blink_counter = 0
last_blink_time = 0
blink_reset_time = 3

# -----------------------------
# Mediapipe FaceMesh
# -----------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cam = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size()

blink_start = None
last_click_blink = 0


while True:

    ret, frame = cam.read()

    if not ret:
        break

    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    output = face_mesh.process(rgb)

    frame_h, frame_w, _ = frame.shape

    if output.multi_face_landmarks:

        landmarks = output.multi_face_landmarks[0].landmark

        # -----------------------------
        # IRIS POSITION (CURSOR CONTROL)
        # -----------------------------
        iris = landmarks[474]

        iris_x = int(iris.x * frame_w)
        iris_y = int(iris.y * frame_h)

        cv2.circle(frame,(iris_x,iris_y),5,(0,255,0),-1)

        screen_x = np.interp(iris_x,[100,frame_w-100],[0,screen_w])
        screen_y = np.interp(iris_y,[100,frame_h-100],[0,screen_h])

        pyautogui.moveTo(screen_x,screen_y)

        # -----------------------------
        # BLINK DETECTION
        # -----------------------------
        top = landmarks[159]
        bottom = landmarks[145]

        top_y = int(top.y * frame_h)
        bottom_y = int(bottom.y * frame_h)

        if abs(top_y - bottom_y) < 5:

            if blink_start is None:
                blink_start = time.time()

        else:

            if blink_start is not None:

                duration = time.time() - blink_start
                blink_start = None

                # -----------------------------
                # RIGHT CLICK
                # -----------------------------
                if duration > 1:

                    pyautogui.rightClick()
                    action = "RIGHT CLICK"

                # -----------------------------
                # DOUBLE CLICK
                # -----------------------------
                elif time.time() - last_click_blink < 0.5:

                    pyautogui.doubleClick()
                    action = "DOUBLE CLICK"

                # -----------------------------
                # LEFT CLICK
                # -----------------------------
                else:

                    pyautogui.click()
                    action = "LEFT CLICK"

                last_click_blink = time.time()

                # -----------------------------
                # COUNT BLINK FOR LOCK
                # -----------------------------
                blink_counter += 1
                last_blink_time = time.time()

                cv2.putText(frame,action,(50,100),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

        # -----------------------------
        # RESET BLINK COUNT
        # -----------------------------
        if time.time() - last_blink_time > blink_reset_time:
            blink_counter = 0

        # -----------------------------
        # SHOW BLINK COUNT
        # -----------------------------
        cv2.putText(frame,f"Blinks: {blink_counter}",(50,150),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2)

        # -----------------------------
        # LOCK SYSTEM
        # -----------------------------
        if blink_counter >= LOCK_BLINK_COUNT:

            cv2.putText(frame,"SYSTEM LOCKING",(200,200),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

            cv2.imshow("Enhanced Eye Gaze Mouse Control",frame)
            cv2.waitKey(1000)

            os.system("rundll32.exe user32.dll,LockWorkStation")

            blink_counter = 0

    cv2.imshow("Enhanced Eye Gaze Mouse Control",frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()