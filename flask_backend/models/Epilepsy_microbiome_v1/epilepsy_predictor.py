import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression

# Load the classifier and feature names and encoder
clf = joblib.load('epilepsy_classifier.pkl')
feature_names = joblib.load('feature_names.pkl')
encoder = joblib.load('encoder.pkl')

# Load the new data
patient_data = pd.read_excel('single_patient_sample.xlsx')

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
patient_data = patient_data.reindex(columns=feature_names)

# Make a prediction
prediction = clf.predict(patient_data)

# Decode the result
decoded_result = encoder.inverse_transform(prediction)
