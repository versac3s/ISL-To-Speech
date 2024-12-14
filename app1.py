import cv2
import mediapipe as mp
import copy
import itertools
from tensorflow import keras
import numpy as np
import pandas as pd
import string
from flask import Flask, render_template, Response, jsonify, request
import time
from gtts import gTTS
import os

app = Flask(__name__)

model_path = os.path.join(os.getcwd(), 'sign-language', 'models', 'model.h5')


model = keras.models.load_model(model_path)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

alphabet =  ['1', '2', '3', '4', '5', '6', '7', '8', '9'] + list(string.ascii_uppercase)

# Variable to store the sequence of detected letters
detected_text = ""
last_detected_time = time.time()  # Track the time when the last letter was detected
detection_delay = 5.0 

# Functions
def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point.append([landmark_x, landmark_y])

    return landmark_point

def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list

def generate_frames():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set the width of the video capture
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set the height of the video capture

    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:
        global detected_text  # To access the global text variable
        global last_detected_time  # To track the last detection time
        while True:
            success, image = cap.read()
            if not success:
                break

            # Flip the image horizontally for a selfie-view display
            image = cv2.flip(image, 1)

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            debug_image = copy.deepcopy(image)

            detected_letter = None  # Variable to hold the detected letter

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmark_list = calc_landmark_list(debug_image, hand_landmarks)
                    pre_processed_landmark_list = pre_process_landmark(landmark_list)
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

                    # Convert landmark data into DataFrame for prediction
                    df = pd.DataFrame(pre_processed_landmark_list).transpose()

                    # Predict the sign language
                    predictions = model.predict(df, verbose=0)
                    predicted_classes = np.argmax(predictions, axis=1)
                    detected_letter = alphabet[predicted_classes[0]]
           
            if detected_letter and (time.time() - last_detected_time > detection_delay):
                detected_text += detected_letter
                last_detected_time = time.time()  # Update the last detection time


            # Convert image to JPEG format for Flask display
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/')
def welcome():
    return render_template('welcomePage.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detected_text')
def get_detected_text():
    global detected_text
    return jsonify({'detected_text': detected_text})

@app.route('/reset_detected_text', methods=['POST'])
def reset_detected_text():
    global detected_text
    detected_text = ""  # Clear the detected text
    return '', 204  # Return HTTP 204 No Content

@app.route('/delete_last_letter', methods=['POST'])
def delete_last_letter():
    global detected_text
    if detected_text:
        detected_text = detected_text[:-1]  # Remove the last letter
        return jsonify({'detected_text': detected_text})  # Return updated text
    else:
        return jsonify({'error': 'No text to delete'}), 400
@app.route('/add_space', methods=['POST'])
def add_space():
    global detected_text
    detected_text += " "  # Add space to the detected text
    return '', 204  # Return HTTP 204 No Content


if __name__ == '__main__':
    app.run(debug=True)
