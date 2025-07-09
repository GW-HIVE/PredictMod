import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

SELECTED_FEATURES = [
    'blood_glucose_value',
    'glucose_rollmean_1h',
    'glucose_rollstd_1h',
    'glucose_diff',
    'hour',
    'is_meal_time',
    'is_night'
]

EXPECTED_LEN = 2138

class Track2Better_Handler:
    def __init__(self):
        self.model = load_model(
            "./models/Predictmod_Track2Better/lstm_binary_model.h5"
        )

    def make_prediction(self, patient_data):

        patient_data = patient_data.sort_values("time_index")

        X_input = patient_data[SELECTED_FEATURES].values.reshape(1, EXPECTED_LEN, len(SELECTED_FEATURES))  # (1, 2138, 7)
        
        y_pred_prob = self.model.predict(X_input)[0][0]
        prediction = int(y_pred_prob > 0.5)

        return {
            "result": "This patient was classified as '{}'".format(
                "True Healthy" if prediction == 1 else "Not healthy"
            )
        }
