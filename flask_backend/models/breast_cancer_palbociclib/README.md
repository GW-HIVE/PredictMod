# Breast Cancer Palbociclib Model
## Data Source
The breast cancer data set was provided by Wenge Zhu,Ph.D. Department of Biochemistry and Molecular Medicine The George Washington University School of Medicine and Health Science.
This was used as a training set to generate a SMOTE balance dataset of 100 patients for prediciton of resistance to palbociclib based treatment of breast cancer.

## Training Dataset
The training dataset consists of ~30 patients and ~30,000 gene symbols across baseline, C1D1, and C1D15 measurments.

## Classifier and Predictor
### Classifier Code
#### Preprocessing
- Load Data: The code imports pandas to read the training data from an Excel file named "[insert file name].xlsx".
- Feature Extraction: Features (X) and labels (y) are extracted from the dataset. Features start from the [insert column number] column, and labels are assumed to be in the [insert column number] column.
- Label Encoding: Labels are converted to numerical values using LabelEncoder.
- Train-Test Split: The data is split into training and testing sets using train_test_split from sklearn.model_selection. The testing set size is set to [insert percentage]%.
- Feature Scaling: The features are standardized using StandardScaler from sklearn.preprocessing.
#### Model Training
- Classifier Selection: A RandomForestClassifier classifier is chosen based on performance compared to other models
- Training: The classifier is trained on the standardized training data.
- Serialization: The trained classifier, feature names, and label encoder are serialized and saved as .pkl files using joblib.
#### Model Evaluation
Prediction: Predictions are made on the test set using the trained classifier.
Performance Evaluation: Accuracy, Confusion Matrix, and Classification Report are calculated using accuracy_score, confusion_matrix, and classification_report from sklearn.metrics.
### Predictor
#### Preprocessing
- Load Model: The pre-trained classifier, feature names, and label encoder are loaded from their respective .pkl files.
- Load New Data: The predictor code imports pandas to read new patient data from an Excel file named "flask_backend\models\breast_cancer_palbociclib\filtered_C0D0_reduced.csv".
- Handle Extra Columns: Extra columns in the new data are either dropped or ignored, with a warning message printed.
- Reorder Columns: The columns of the new data are reordered to match the order of features used during training.
#### Prediction
- Make Prediction: The loaded classifier predicts the label for the new patient data.
Intervention & Outcomes
- Responder: Patient data suggests positive response to Palbociclib prior to intervention treatment
- Non-Responder: Patient data suggests resistance to Palbociclib prior to intervention treatment
### Algorithm & Model Performance
- Algorithm: RandomForestClassifier
- Model Accuracy: 0.93
- ROC-AUC: 0.83
