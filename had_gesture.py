import cv2
import mediapipe as mp
import serial
import time

# Initialize serial communication with Arduino
try:
    arduino = serial.Serial('COM4', 9600)  # Replace 'COM4' with your actual port
    time.sleep(2)  # Wait for the connection to initialize
except serial.SerialException as e:
    print(f"Serial error: {e}")
    arduino = None

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Function to count open fingers
def count_fingers(landmarks):
    count = 0
    tips = [4, 8, 12, 16, 20]
    for tip in tips[1:]:  # Ignore thumb for simplicity
        if landmarks[tip].y < landmarks[tip - 2].y:
            count += 1
    return count

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            finger_count = count_fingers(landmarks)

            palm_x = landmarks[9].x
            if palm_x < 0.4:
                servo_direction = "L"
            elif palm_x > 0.6:
                servo_direction = "R"
            else:
                servo_direction = "C"

            fan_speed = finger_count * 25  # 0 to 100
            command = f"F{fan_speed}\nS{servo_direction}\n"

            if arduino:
                arduino.write(command.encode())

            cv2.putText(frame, f"Fingers: {finger_count}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f"Palm: {servo_direction}", (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
 
    cv2.imshow("Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()