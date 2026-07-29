import cv2
import numpy as np
import pyautogui
import time
import math
from collections import deque
import mediapipe as mp
import tensorflow as tf  # ⬅️ new for TFLite

# ------------------ CONFIG ------------------
IMG_WIDTH, IMG_HEIGHT = 224, 224
EXPRESSIONS = ['mouth_open', 'neutral', 'tongue_out']
import os
import sys

if getattr(sys, 'frozen', False):
    # Running as a bundled app
    base_path = sys._MEIPASS
else:
    # Running in normal Python
    base_path = os.path.abspath(".")

MODEL_PATH = os.path.join(base_path, "assets", "expression_pointer.tflite")  # ⬅️ updated path
CAMERA_INDEX = 0

BLINK_THRESHOLD = 0.21
BLINK_FRAMES_REQUIRED = 4
SCROLL_CONFIDENCE_THRESHOLD = 0.85
PREDICTION_SMOOTHING_WINDOW = 15

AMPLIFICATION = 5.3
DEADZONE_THRESHOLD = 0.01
SMOOTHING_ALPHA = 0.13
EYEBROW_THRESHOLD = 0.05
BLINK_COOLDOWN = 1.0

# ------------------ INIT ------------------
pyautogui.FAILSAFE = False
screen_width, screen_height = pyautogui.size()
screen_center_x, screen_center_y = screen_width // 2, screen_height // 2
pyautogui.moveTo(screen_center_x, screen_center_y)

cap = cv2.VideoCapture(CAMERA_INDEX)
print(" Position yourself... Starting in 5 seconds")
time.sleep(5)

# 🔁 Load TFLite model
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True,
                                   min_detection_confidence=0.5, min_tracking_confidence=0.5)

NOSE_TIP = 1
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
LEFT_EYE_TOP = 159
LEFT_EYEBROW_BOTTOM = 105
RIGHT_EYE_TOP = 386
RIGHT_EYEBROW_BOTTOM = 334

neutral_nose_x, neutral_nose_y = None, None
smooth_x, smooth_y = screen_center_x, screen_center_y
blink_counter_left = 0
blink_counter_right = 0
last_left_click_time = 0
last_right_click_time = 0
eyebrow_raised = False
control_enabled = True

def euclidean(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def calculate_ear(landmarks, indices, w, h):
    coords = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in indices]
    v1 = euclidean(coords[1], coords[5])
    v2 = euclidean(coords[2], coords[4])
    h_len = euclidean(coords[0], coords[3])
    return (v1 + v2) / (2.0 * h_len)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        h, w, _ = frame.shape

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            left_dist = landmarks[LEFT_EYEBROW_BOTTOM].y - landmarks[LEFT_EYE_TOP].y
            right_dist = landmarks[RIGHT_EYEBROW_BOTTOM].y - landmarks[RIGHT_EYE_TOP].y
            if left_dist > EYEBROW_THRESHOLD and right_dist > EYEBROW_THRESHOLD:
                if not eyebrow_raised:
                    control_enabled = not control_enabled
                    eyebrow_raised = True
                    print(f" Control Enabled: {control_enabled}")
            else:
                eyebrow_raised = False

            if control_enabled:
                nose = landmarks[NOSE_TIP]
                if neutral_nose_x is None:
                    neutral_nose_x, neutral_nose_y = nose.x, nose.y
                    pyautogui.moveTo(screen_center_x, screen_center_y)
                    print(" Head tracking started. Neutral locked.")
                    time.sleep(0.3)
                    continue

                dx = nose.x - neutral_nose_x
                dy = nose.y - neutral_nose_y
                if abs(dx) < DEADZONE_THRESHOLD: dx = 0
                if abs(dy) < DEADZONE_THRESHOLD: dy = 0

                target_x = screen_center_x + dx * AMPLIFICATION * screen_width
                target_y = screen_center_y + dy * AMPLIFICATION * screen_height
                smooth_x = int(SMOOTHING_ALPHA * target_x + (1 - SMOOTHING_ALPHA) * smooth_x)
                smooth_y = int(SMOOTHING_ALPHA * target_y + (1 - SMOOTHING_ALPHA) * smooth_y)
                pyautogui.moveTo(smooth_x, smooth_y)

                left_ear = calculate_ear(landmarks, LEFT_EYE, w, h)
                right_ear = calculate_ear(landmarks, RIGHT_EYE, w, h)

                if left_ear < BLINK_THRESHOLD:
                    blink_counter_left += 1
                else:
                    if blink_counter_left >= BLINK_FRAMES_REQUIRED and (time.time() - last_left_click_time > BLINK_COOLDOWN):
                        pyautogui.click(button='left')
                        print("LEFT CLICK")
                        last_left_click_time = time.time()
                    blink_counter_left = 0

                if right_ear < BLINK_THRESHOLD:
                    blink_counter_right += 1
                else:
                    if blink_counter_right >= BLINK_FRAMES_REQUIRED and (time.time() - last_right_click_time > BLINK_COOLDOWN):
                        pyautogui.click(button='right')
                        print("RIGHT CLICK")
                        last_right_click_time = time.time()
                    blink_counter_right = 0

                # ✅ EXPRESSION SCROLL BLOCK
                xs = [int(landmark.x * w) for landmark in landmarks]
                ys = [int(landmark.y * h) for landmark in landmarks]
                x_min, x_max = max(min(xs) - 10, 0), min(max(xs) + 10, w)
                y_min, y_max = max(min(ys) - 10, 0), min(max(ys) + 10, h)

                face_roi = frame[y_min:y_max, x_min:x_max]

                if face_roi.size > 0:
                    resized = cv2.resize(face_roi, (IMG_WIDTH, IMG_HEIGHT))
                    rgb_input = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                    normalized = rgb_input.astype("float32") / 255.0
                    input_data = np.expand_dims(normalized, axis=0).astype(np.float32)

                    interpreter.set_tensor(input_details[0]['index'], input_data)
                    interpreter.invoke()
                    prediction = interpreter.get_tensor(output_details[0]['index'])

                    predicted_class = np.argmax(prediction)

                    if predicted_class < len(EXPRESSIONS):
                        expression = EXPRESSIONS[predicted_class]
                        if expression == 'mouth_open':
                            pyautogui.scroll(-100)
                            print("Scroll Down")
                        elif expression == 'tongue_out':
                            pyautogui.scroll(100)
                            print("Scroll Up")
                    else:
                        print(f" Invalid expression index: {predicted_class}")

        cv2.imshow("Expression Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

except KeyboardInterrupt:
    print("\n🛑 Exiting...")

finally:
    cap.release()
    cv2.destroyAllWindows()
