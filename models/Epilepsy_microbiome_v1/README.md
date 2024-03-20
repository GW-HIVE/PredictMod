# Data Preprocessing, Algorithm Selection, and Model Evaluation for Epilepsy Classifier
## Data Source
Epilepsy data set was provided by Department of Veterians Affairs. This was used as a training set to generate a 500 patient dataset for the epilepsy gut microbiome classifier and predictor 

## Training Dataset
The training dataset consists of 500 patients and 188 variables.

## Classifier and Predictor
### Classifier Code:
#### Preprocessing:
- Load Data: The code imports pandas to read the training data from an Excel file named "epilepsy_data_500.xlsx".
- Feature Extraction: Features (X) and labels (y) are extracted from the dataset. Features start from the 4th column, and labels are assumed to be in the 3rd column.
- Label Encoding: Labels are converted to numerical values using LabelEncoder.
- Train-Test Split: The data is split into training and testing sets using train_test_split from sklearn.model_selection. The testing set size is set to 20%.
- Feature Scaling: The features are standardized using StandardScaler from sklearn.preprocessing.
- Model Training:
#### Classifier Selection: A Logistic Regression classifier is chosen.
- Training: The classifier is trained on the standardized training data.
- Serialization: The trained classifier, feature names, and label encoder are serialized and saved as .pkl files using joblib.
#### Model Evaluation:
- Prediction: Predictions are made on the test set using the trained classifier.
- Performance Evaluation: Accuracy, Confusion Matrix, and Classification Report are calculated using accuracy_score, confusion_matrix, and classification_report from sklearn.metrics.
### Predictor
#### Preprocessing:
- Load Model: The pre-trained classifier, feature names, and label encoder are loaded from their respective .pkl files.
- Load New Data: The predictor code imports pandas to read new patient data from an Excel file named "single_patient_sample.xlsx".
- Handle Missing Columns: Missing columns in the new data are filled with 0 or appropriate values.
- Handle Extra Columns: Extra columns in the new data are either dropped or ignored, with a warning message printed.
- Reorder Columns: The columns of the new data are reordered to match the order of features used during training.
#### Prediction:
- Make Prediction: The loaded classifier predicts the label for the new patient data.
- Decode Prediction: The predicted label is decoded using the label encoder.

## Intervention & Outcomes
- Responder Status: Patients diagnosed with reduced epileptic seizures in response to keto diet
- Nonresponder Status: Patients not diagnosed with reduced epileptic seizures in response to keto diet

## Algorithm & Model Performance
Algorithm: Logistic Regression (LR)
Model Accuracy: 87%

