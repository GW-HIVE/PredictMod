import pandas as pd
import numpy as np
import joblib

def predict_patient(patient_filename='single_patient_mdclone_exercise.csv'):
    # Load the trained model, scaler, and feature names
    model_data = joblib.load('Diabetes_EHR_classifier_and_features.pickle')
    classifier = model_data['classifier']
    scaler = model_data['scaler']
    feature_names = model_data['feature_names']

    # Load the single patient's data
    patient_df = pd.read_csv(patient_filename)

    # Ensure the patient data has the same features (and order)
    if set(feature_names) != set(patient_df.columns):
        raise ValueError("Mismatch in feature names between model and patient data.")

    # Reorder columns to match training feature order
    patient_df = patient_df[feature_names]

    # Scale the patient's features
    patient_scaled = scaler.transform(patient_df)

    # Predict the outcome
    prediction = classifier.predict(patient_scaled)
    probability = classifier.predict_proba(patient_scaled) if hasattr(classifier, "predict_proba") else None

    # Display result
    if prediction[0] == 0:
        print("Patient is predicted to be non-responder to exercise intervention.")
    else:
        print("Patient is predicted to be responder to exercise intervention.")

# Call the predict_patient function
predict_patient('single_patient_mdclone_exercise.csv')
