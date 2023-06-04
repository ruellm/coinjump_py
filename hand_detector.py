import mediapipe as mp
import cv2

class BoundingBox:
    def __init__(self,  x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

class HandDetector:
    def __init__(self, detection_confidence=0.5, tracking_confidence=0.5):
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence)
        self.draw_util = mp.solutions.drawing_utils
        self.bboxes = []
       
    def detect_hand(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        if results.multi_hand_landmarks:
            self.bboxes = []
            for hand_landmarks in results.multi_hand_landmarks:
                # Calculate bounding box coordinates
                x_min, y_min, x_max, y_max = self.get_bounding_box(hand_landmarks, image.shape)
                # Draw rectangle around the hand
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 255), 2)

                fx_min, fy_min, fx_max, fy_max = self.get_bounding_box_flipped(hand_landmarks, image.shape)
                bbox = BoundingBox(fx_min, fy_min, fx_max, fy_max)
                self.bboxes.append(bbox)

        return image

    def get_bounding_box(self, hand_landmarks, image_shape):
        x_min, x_max = float('inf'), 0
        y_min, y_max = float('inf'), 0

        for landmark in hand_landmarks.landmark:
            x, y = int(landmark.x * image_shape[1]), int(landmark.y * image_shape[0])
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y

        return x_min, y_min, x_max, y_max
    
    def get_bounding_box_flipped(self, hand_landmarks, image_shape):
        x_min, x_max = float('inf'), 0
        y_min, y_max = float('inf'), 0

        for landmark in hand_landmarks.landmark:
            x, y = int(landmark.x * image_shape[1]), int(landmark.y * image_shape[0])
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y

        # Adjust coordinates for flipped image
        x_min, x_max = image_shape[1] - x_max, image_shape[1] - x_min

        return x_min, y_min, x_max, y_max
    
    def is_hand_inside_rectangle(self, rect_x, rect_y, rect_width, rect_height):
        for bbox in self.bboxes:
            if (
                rect_x >= bbox.x_min
                and rect_y >= bbox.y_min
                and rect_x + rect_width <= bbox.x_max
                and rect_y + rect_height <= bbox.y_max
            ):
                return True
        return False