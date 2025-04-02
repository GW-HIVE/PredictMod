import pandas as pd
import joblib

def predict_patient(patient_file_path = 'single_patient_semaglutide.xlsx',pkl_path = 'Semaglutide_EHR_classifier_and_features.pickle'):
    # Load the dictionary from the pickle file
    pkl_path = joblib.load('Semaglutide_EHR_classifier_and_features.pickle')

    # Extract the classifier and feature names from the dictionary
    classifier = pkl_path['classifier']
    feature_names = pkl_path['feature_names']

    # Read the Excel file
    try:
        patient_pkl_path = pd.read_excel(patient_file_path)
    except Exception as e:
        print(f'Error reading the file: {e}')
        exit()

    # Check for missing columns in the new pkl_path
    missing_cols = set(feature_names) - set(patient_pkl_path.columns)
    for c in missing_cols:
        patient_pkl_path[c] = 0  # or some other value that makes sense in your context

    # Check for extra columns in the new pkl_path
    extra_cols = set(patient_pkl_path.columns) - set(feature_names)
    if extra_cols:
        print(f"Warning: Found extra columns in the new pkl_path that were not in the training pkl_path: {extra_cols}")
        patient_pkl_path = patient_pkl_path.drop(columns=extra_cols)

    # Reorder the columns of the new pkl_path
    patient_pkl_path_sort = patient_pkl_path.reindex(columns=feature_names)
    if not patient_pkl_path.equals(patient_pkl_path_sort):
        print("Message: patient pkl_path features were sorted to match the order of model features")

    # Make a prediction
    prediction = classifier.predict(patient_pkl_path_sort)
    if prediction == 1:
        print('Patient is likely to be responsive to Semaglutide treatment')
    else:
        print('Patient is unlikely to be responsive to Semaglutide treatment')

predict_patient('single_patient_semaglutide.xlsx','Semaglutide_EHR_classifier_and_features.pickle')
