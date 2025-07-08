# Import libraries
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

# Constants
MODEL_PATH = "lstm_binary_model.h5"
CSV_PATH = "test_set.csv"

EXPECTED_LEN = 2138
SELECTED_FEATURES = [
    'blood_glucose_value',
    'glucose_rollmean_1h',
    'glucose_rollstd_1h',
    'glucose_diff',
    'hour',
    'is_meal_time',
    'is_night'
]

# Step 1: Load the trained LSTM model
model = load_model(MODEL_PATH)

# Step 2: Load and validate the unseen participant data
df = pd.read_csv(CSV_PATH)

# Ensure the data contains only one participant from Group 2
assert df['study_group'].nunique() == 1, "CSV must contain only one participant"

# Step 3: Preprocess the data
df['glucose_rollstd_1h'] = df['glucose_rollstd_1h'].fillna(0)
df = df.sort_values("time_index")

if len(df) != EXPECTED_LEN:
    raise ValueError(f"Incomplete time-series: expected {EXPECTED_LEN}, got {len(df)}")

X_input = df[SELECTED_FEATURES].values.reshape(1, EXPECTED_LEN, len(SELECTED_FEATURES))  # (1, 2138, 7)

# Step 4: Make prediction
y_pred_prob = model.predict(X_input)[0][0]
y_pred_class = int(y_pred_prob > 0.5)

# Step 5: Display results
print(f"Prediction Probability: {y_pred_prob:.4f}")
print(f"Predicted Class: {'True-Healthy (1)' if y_pred_class == 1 else 'Not Healthy (0)'}")

# Step 6: Classification sanity check
if y_pred_class == 1:
    print("WARNING: Group 2 participant misclassified as True-Healthy!")
else:
    print("Correct: Group 2 participant not classified as healthy.")
