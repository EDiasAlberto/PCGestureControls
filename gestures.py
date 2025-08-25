import cv2
from math import hypot
from enum import Enum
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

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
        self.cap = cv2.VideoCapture(camera_index)
        self.hands = mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence)
        self.positionHandler = positionHandler

    def distance(self, a, b):
        return hypot(a.x - b.x, a.y - b.y)

    def average_pos(self):
        keyPoints = [[self.landmarks[point.value].x, self.landmarks[point.value].y] for point in PalmPoints]
        return (np.mean(keyPoints, axis=0))

    def run(self):
        self.frameCount = 0
        while self.cap.isOpened():
            self.frameCount += 1
            if self.frameCount % 2 == 0:
                self.frameCount == 0    
                continue
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                self.isPinching = self.distance(hand_landmarks.landmark[THUMB_TIP], hand_landmarks.landmark[INDEX_TIP]) < 0.05

                self.isSecondaryPinching = self.distance(hand_landmarks.landmark[THUMB_TIP], hand_landmarks.landmark[PINKY_TIP]) < 0.05

                self.landmarks = hand_landmarks.landmark
                palmPosition = self.average_pos()
                self.positionHandler(palmPosition[0], palmPosition[1], self.isPinching, self.isSecondaryPinching)
                # draw a circle at the palm position
                h, w, c = image.shape
                cv2.circle(image, (int(palmPosition[0] * w), int(palmPosition[1] * h)), 10, (255, 0, 0), -1)
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
        self.cap.release()

