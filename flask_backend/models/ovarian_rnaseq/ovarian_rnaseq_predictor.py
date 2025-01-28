import joblib
import pandas as pd
import numpy as np

# Load the saved model
model_data = joblib.load('ovarian_rnaseq_model.pkl')
patient_input = pd.read_excel('ovarian_RNAseq_single_patient.xlsx', header=None)
# Extract the feature names from the first row (index 0)
patient_features = patient_input.iloc[1:, 0].values  # The first row contains the feature names

patient_data = patient_input.iloc[1:, 1:].reset_index(drop=True) # The rest is data
# Extract the classifier and feature names from the model data
clf = model_data['model']
# Extract the normalizer from the model data
normalizer = model_data['normalizer']
# Extract the feature names from the model data
feature_names = np.array(model_data['feature_names'])

# Normalize the patient data before prediction
patient_data_normalized = normalizer.transform(patient_data.T)

# Predict the outcome using the model
prediction = clf.predict(patient_data_normalized)

# Output the result
print(f"The predicted outcome for the patient is: {prediction[0]}")
