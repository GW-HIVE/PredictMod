# Data Preprocessing, Algorithm Selection, and Model Evaluation for Diabetes Classifier
## Data Source
Synthea ([https://synthea.mitre.org/]) is a synthetic patient data platform that provides patient data without compromising personal patient information. This was used as a training set to generate a 1000 patient dataset for the diabetes EHR classifier and predictor 

## Training Dataset
The training dataset consists of 1000 patients and 8 variables.

## Classifier and Predictor
### Classifier Code:
The classifier code takes patient data and labels, splits the data into training and testing sets, and trains a Decision Tree Classifier (DTC) on the training data. The trained classifier is then serialized and stored as a .pkl file for later use. During training, the accuracy of the classifier is calculated and printed. When taking single patient data for prediction, the trained classifier is loaded from the .pkl file, and the input data is reshaped to match the classifier's requirements. The trained classifier then predicts whether the patient is responsive or non-responsive based on the input data, and the result is printed along with the accuracy of the classifier during training.

### Predictor Code:
The predictor code loads the pre-trained Decision Tree Classifier (DTC) from the .pkl file. It prompts the user to provide the file path for the single patient input data. The input data is then read from an Excel file. The predictor reshapes the input data to match the classifier's requirements and uses the loaded classifier to predict whether the patient is responsive or non-responsive based on the input data. The prediction result is printed to the console.

## Intervention & Outcomes
Intervention was stated as standard diabetetic exercise intervention in the Synthea database
- Responder Status: Patients diagnosed with diabetes or prediabetes during doctor visits.
- Nonresponder Status: Patients not diagnosed with diabetes or prediabetes during doctor visits.

## Algorithm & Model Performance
Algorithm: Decision Tree Classifier (DTC)
Model Accuracy: 0.931
