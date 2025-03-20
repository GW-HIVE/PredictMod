import pickle
import pandas as pd

# Load the model
model_filename = "prediabetes_proteomics_model.pkl"
with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Load the single patient data
csv_filename = "prediabetes_proteomics_single_patient.csv"
data = pd.read_csv(csv_filename)

# Ensure data has the right features 
expected_features = model.feature_names_in_  # Requires scikit-learn 1.0+
data = data[expected_features]  # Keep only necessary features

# Make prediction
prediction = model.predict(data)

# Save prediction to a text file
output_filename = "prediction_result.txt"
with open(output_filename, 'w') as output_file:
    output_file.write(f"Predicted outcome: {prediction[0]}\n")
