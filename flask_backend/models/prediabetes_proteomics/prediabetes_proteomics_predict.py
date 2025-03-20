import pickle
import pandas as pd

# Load the model
model_filename = "prediabetes_proteomics_model.pkl"
with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Load the single patient data
csv_filename = "prediabetes_proteomics_single_patient.csv"
data = pd.read_csv(csv_filename)

# Ensure data has the right features (assuming the model was trained on specific columns)
expected_features = model.feature_names_in_  # Requires scikit-learn 1.0+
data = data[expected_features]  # Keep only necessary features

# Make prediction
prediction = model.predict(data)

# Print the prediction
print("Predicted outcome:", prediction[0])
