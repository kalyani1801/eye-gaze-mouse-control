import pyautogui

pyautogui.FAILSAFE = False


class CursorController:

    def __init__(self):

        self.speed = 40


    def move(self, direction):

        x, y = pyautogui.position()

        if direction == "LEFT":
            x -= self.speed

        elif direction == "RIGHT":
            x += self.speed

        elif direction == "UP":
            y -= self.speed

        elif direction == "DOWN":
            y += self.speed

        pyautogui.moveTo(x, y, duration=0.05)


    def click(self, action):

        if action == "LEFT_CLICK":
            pyautogui.click()

        elif action == "DOUBLE_CLICK":
            pyautogui.doubleClick()

        elif action == "RIGHT_CLICK":
            pyautogui.rightClick()