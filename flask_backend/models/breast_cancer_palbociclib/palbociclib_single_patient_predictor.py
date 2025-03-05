import pandas as pd
import numpy as np
import pickle

def load_data_and_model(file_path, model_path):
    df = pd.read_csv(file_path, header=None)

    with open(model_path, "rb") as f:
        data = pickle.load(f)

    model = data["model"]
    feature_headers = data["feature_headers"]
    return model, feature_headers, df

def check_single_patient(feature_headers, single_patient): 
    print(type(single_patient))
    list_2_df = (pd.DataFrame(feature_headers).reshape(1, -1))
    print(single_patient.iloc[:, 0].shape)
    print(list_2_df.shape)
    # Check for missing features
    missing_features = set(list_2_df) - set(single_patient.columns)
    if missing_features:
        raise ValueError(f"Missing features in single_patient: {missing_features}")

    # Check for extra features (remove them)
    extra_features = set(single_patient.columns) - set(list_2_df)
    print("Feature Headers:", feature_headers)
    print("Single Patient Columns:", single_patient.columns.tolist())

    if extra_features:
        print(f"Warning: Extra features found in single_patient, removing: list{extra_features}")
        single_patient = single_patient.drop(columns=extra_features)
    print("checking complete")

model, model_features, single_patient = load_data_and_model("single_patient_data.csv", "trained_model_and_headers.pkl")
patient = np.array(single_patient.iloc[:, 1:]).reshape(1, -1)
prediction = model.predict(patient)[0]
if prediction == 0:
    print(f"Predicted Outcome: Succesful response to palbociclib")
else:
    print(f"Predicted Outcome: Unsuccesful response to palbociclib (resistance)")