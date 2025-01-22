import joblib
import pandas as pd

# Load the saved model
model_data = joblib.load('ovarian_rnaseq_model.pkl')
patient_input = pd.read_excel('ovarian_RNAseq_single_patient.xlsx', header=None)
patient_data = patient_input.iloc[1:, 1:].reset_index(drop=True)
# patient_features = patient_data.iloc[1:, 0].values
# Extract the classifier and feature names from the model data
clf = model_data['model']

# Predict the outcome using the model
prediction = clf.predict(patient_data.T)

# Output the result
print(f"The predicted outcome for the patient is: {prediction[0]}")
