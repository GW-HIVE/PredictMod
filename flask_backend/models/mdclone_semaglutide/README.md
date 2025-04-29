# Semaglutide Responsiveness Classifier and Predictor

## Data Source
The dataset used for this project consists of curated clinical data from patients treated with **Semaglutide**, a GLP-1 receptor agonist prescribed for Type 2 diabetes and weight management. This dataset contains anonymized patient features and response labels, prepared for supervised machine learning training.

## Training Dataset
The training dataset contains structured data from semaglutide-treated patients, including a balanced mix of responders and non-responders. Feature variables include clinical and lifestyle indicators relevant to treatment response prediction.

## Classifier and Predictor

### Classifier Code:
The classifier code reads the patient dataset and corresponding response labels, scales the features using `StandardScaler`. A **XGBoost Classifier ** is trained on the processed data, and its performance is evaluated using accuracy and ROC metrics. The final model, along with the scaler and feature names, is saved as a `.pkl` file using `joblib` for use in future predictions. The model achieved an accuracy of **70%** during evaluation on the test set.

### Predictor Code:
The predictor script loads the saved `.pkl` file containing the trained classifier, scaler, and feature names. It reads a new patient's data from an Excel file, verifies that all required features are present (adding any missing ones with a default value), drops any extraneous columns, and ensures the feature order matches the training data. The data is then scaled using the same scaler, and the classifier is used to predict whether the patient is likely or unlikely to respond to Semaglutide treatment. The result is printed to the console.

## Intervention & Outcomes
Patients in the training set were prescribed Semaglutide as part of a therapeutic intervention for metabolic disease management.
- **Responder Status**: Patients who demonstrated a favorable clinical response to Semaglutide (e.g., improved glycemic control, weight loss).
- **Nonresponder Status**: Patients who did not show significant improvement under Semaglutide treatment.

## Algorithm & Model Performance
- **Algorithm**: Decision Tree Classifier (DTC)  
- **Model Accuracy**: 0.70
- **Top 5 Predictive Features**:

| Feature                                      | Importance |
|----------------------------------------------|------------|
| platelet count-result numeric (original)     | 0.0696     |
| hematocrit-result numeric (original)         | 0.0659     |
| heart rate-heart rate                        | 0.0635     |
| chloride_copy-result numeric (original)      | 0.0592     |
| total cholesterol-result numeric (original)  | 0.0555     |

