import cv2
from math import hypot
from enum import Enum
import platform 
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

FRAMESKIP_COUNT = 1
FRAMESKIP_MAX = 10

THUMB_TIP = 4
INDEX_TIP = 8
PINKY_TIP = 20

class PalmPoints(Enum):
    WRIST = 0
    INDEX_MCP = 5
    MIDDLE_MCP = 9
    RING_MCP = 13
    PINKY_MCP = 17

class GestureTracking:

    def __init__(self, positionHandler, camera_index=0, detection_confidence=0.5, tracking_confidence=0.5):
        self.isPinching = False
        # Use platform-appropriate VideoCapture
        if platform.system() == "Windows":
            self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        else:
            self.cap = cv2.VideoCapture(camera_index)
        self.hands = mp_hands.Hands(
            model_complexity=0,
            max_num_hands=1,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence)
        self.positionHandler = positionHandler
        self.palmPosition = (0, 0)

    def distance(self, a, b):
        return hypot(a.x - b.x, a.y - b.y)

    def average_pos(self):
        keyPoints = [[self.landmarks[point.value].x, self.landmarks[point.value].y] for point in PalmPoints]
        return np.round(np.mean(keyPoints, axis=0), 4)

    def run(self, isDrawing=True):
        self.frameCount = 0
        while self.cap.isOpened():
            self.frameCount += 1
            if self.frameCount > FRAMESKIP_MAX:
                self.frameCount = 0
            if self.frameCount % FRAMESKIP_COUNT != 0:
                continue
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image)

            if results.multi_hand_landmarks:
                self.landmarks = results.multi_hand_landmarks[0].landmark
                self.isPinching = self.distance(self.landmarks[THUMB_TIP], self.landmarks[INDEX_TIP]) < 0.05
                self.isSecondaryPinching = self.distance(self.landmarks[THUMB_TIP], self.landmarks[PINKY_TIP]) < 0.05
                self.palmPosition = self.average_pos()
                self.positionHandler(self.palmPosition[0], self.palmPosition[1], self.isPinching, self.isSecondaryPinching)
        self.cap.release()

