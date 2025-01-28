import pandas as pd
import joblib

# Load the dictionary from the pickle file
data = joblib.load('Semaglutide_EHR_classifier_and_features.pickle')

# Extract the classifier and feature names from the dictionary
classifier = data['classifier']
feature_names = data['feature_names']

# Load the single patient data
file_path = 'single_patient_semaglutide.xlsx'

# Read the Excel file
try:
    patient_data = pd.read_excel(file_path)
except Exception as e:
    print(f'Error reading the file: {e}')
    exit()

# Check for missing columns in the new data
missing_cols = set(feature_names) - set(patient_data.columns)
for c in missing_cols:
    patient_data[c] = 0  # or some other value that makes sense in your context

# Check for extra columns in the new data
extra_cols = set(patient_data.columns) - set(feature_names)
if extra_cols:
    print(f"Warning: Found extra columns in the new data that were not in the training data: {extra_cols}")
    patient_data = patient_data.drop(columns=extra_cols)

# Reorder the columns of the new data
patient_data_sort = patient_data.reindex(columns=feature_names)
if not patient_data.equals(patient_data_sort):
    print("Message: patient data features were sorted to match the order of model features")

# Make a prediction
prediction = classifier.predict(patient_data_sort)
print("Prediction:", prediction)
