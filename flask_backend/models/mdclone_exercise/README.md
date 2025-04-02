# Data Preprocessing, Algorithm Selection, and Model Evaluation for Diabetes Classifier

## Data Source
The dataset used in this project was manually curated and loaded from `Exercise_curated.xlsx`, simulating clinical records for diabetes patient classification. This dataset contains anonymized and structured patient records suitable for supervised machine learning training.

## Training Dataset
The training dataset consists of structured features representing patient metrics and a binary label indicating diabetes-related response status. This dataset was balanced during preprocessing to ensure equal representation of both responder and non-responder classes.

## Classifier and Predictor

### Classifier Code:
The classifier script reads the patient dataset and separates it into features and labels. To address class imbalance, the code uses `RandomOverSampler` to balance the dataset. Features are standardized using `StandardScaler`, and a **Decision Tree Classifier (DTC)** is trained on a 60/40 train/test split. The trained classifier, along with the scaler and feature names, is serialized into a `.pkl` file using `joblib` for later prediction use. During training, the model achieved an **accuracy of 84%** and its feature importances are printed for interpretability.

### Predictor Code:
The predictor script loads the pre-trained Decision Tree Classifier and associated scaler from the `.pkl` file. It accepts a new patient's data input file, ensures the feature columns match the expected input structure, and scales the input accordingly. The model then predicts whether the patient is classified as a diabetes responder or non-responder. The result is printed to the console for clinical interpretation or downstream use.

## Intervention & Outcomes
Patients in the training data are labeled based on clinical criteria related to diabetes treatment outcomes.
- **Responder Status**: Patients exhibiting favorable diabetic control or treatment adherence.
- **Nonresponder Status**: Patients not demonstrating desired clinical improvement under the evaluated conditions.

## Algorithm & Model Performance
- **Algorithm**: Decision Tree Classifier (DTC)  
- **Model Accuracy**: 0.84
