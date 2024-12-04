from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import cv2
import mediapipe as mp
import copy
import itertools
from tensorflow import keras
import numpy as np
import pandas as pd
import string
import eventlet

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# Load model
model = keras.models.load_model("C:/Users/d88zx/OneDrive/Desktop/ISL/Indian-Sign-Language-Detection/model.h5")

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

alphabet = ['1','2','3','4','5','6','7','8','9']
alphabet += list(string.ascii_uppercase)

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
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]
        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value
    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list

@app.route('/predict', methods=['POST'])
def predict():
    # This route will accept image input for processing
    data = request.json  # Receiving data from React Frontend

    # Process the data and get the sign language prediction (this can be from webcam image or uploaded images)
    landmark_list = data['landmarks']  # You would process these landmarks
    pre_processed_landmark_list = pre_process_landmark(landmark_list)
    
    df = pd.DataFrame(pre_processed_landmark_list).transpose()
    predictions = model.predict(df, verbose=0)
    predicted_classes = np.argmax(predictions, axis=1)
    label = alphabet[predicted_classes[0]]
    
    return jsonify({"predictedLabel": label})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
