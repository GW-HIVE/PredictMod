import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression

# Load the classifier
clf = joblib.load('Diabetes_classifier.pkl')

# Load the new data
file_path = input('Enter the file path for single patient input (e.g., C:\\Users\\17038\\a_Fall_2023\\work\\Diabetes_EHR_v1\\single_patient_input.xlsx): ')
patient_data = pd.read_excel('single_patient_input.xlsx')

# Read the Excel file
try:
    test_data = pd.read_excel(file_path)
except Exception as e:
    print(f'Error reading the file: {e}')
    exit()

patient_data = test_data.to_numpy()
reshaped_patient = patient_data.reshape((1, 6))
y_hat = clf.predict(reshaped_patient)
# Get the type of the classifier
classifier_type_string = type(clf).__name__
if int(y_hat) == 1:
    outcome = 'Non-Responsive'
else:
    outcome = 'Responsive'
print(f"Patient input data has been predicted to be {outcome} using {classifier_type_string}")
