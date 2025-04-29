import pandas as pd
import joblib

def predict_patient(patient_file_path='single_patient_semaglutide.xlsx',
                    pkl_path='decision_tree_model_bundle.pkl'):
    # Load the dictionary from the pickle file
    model_bundle = joblib.load(pkl_path)

    # Extract classifier, scaler, and feature names
    classifier = model_bundle['model']
    scaler = model_bundle['scaler']
    feature_names = model_bundle['columns']

    # Read the Excel file
    try:
        patient_data = pd.read_csv(patient_file_path)
    except Exception as e:
        print(f'Error reading the file: {e}')
        return

    # Add any missing columns and set them to 0
    missing_cols = set(feature_names) - set(patient_data.columns)
    for col in missing_cols:
        patient_data[col] = 0

    # Drop any extra columns
    extra_cols = set(patient_data.columns) - set(feature_names)
    if extra_cols:
        print(f"Warning: Found extra columns not used by the model: {extra_cols}")
        patient_data = patient_data.drop(columns=extra_cols)

    # Reorder columns to match training feature order
    patient_data = patient_data.reindex(columns=feature_names)

    # Apply the stored scaler
    patient_data_scaled = scaler.transform(patient_data)

    # Make a prediction
    prediction = classifier.predict(patient_data_scaled)
    proba = classifier.predict_proba(patient_data_scaled)[0][1]

    if prediction[0] == 1:
        print(f'Patient is likely to be responsive to Semaglutide treatment (probability: {proba:.2f})')
    else:
        print(f'Patient is unlikely to be responsive to Semaglutide treatment (probability: {proba:.2f})')

# Run prediction
predict_patient('Single_patient_semaglutide.csv', 'decision_tree_model_bundle.pkl')
