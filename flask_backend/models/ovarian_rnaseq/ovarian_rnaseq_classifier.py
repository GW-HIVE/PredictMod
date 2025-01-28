# File: methylation_classifier_with_smote.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.preprocessing import Normalizer
from imblearn.over_sampling import SMOTE
import joblib

# Step 1: Load the data
file_path = 'curated_RNAseq_patient_data.xlsx'  # Replace with the actual file path
data = pd.read_excel(file_path, header=None)

# Step 2: Extract target (y) from the first row and features (X) from the remaining data
y = data.iloc[0, 1:].values  # First row (excluding the first column) as target vector
y = y.astype(int)
X = data.iloc[1:, 1:].reset_index(drop=True)  # All rows except the first row and first column
X = X.T  # Transpose the matrix
normalizer = Normalizer(norm='l1')  # 'l1' ensures row-wise sum = 1
X = normalizer.fit_transform(X)
feature_names = data.iloc[1:, 0].values  # First column as feature names

# Step 4: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=1
)

# Step 5: Apply SMOTE to the training data
desired_class_distribution = {0: 100, 1: 100}  # Adjust as per your need
smote = SMOTE(sampling_strategy=desired_class_distribution, k_neighbors=2, random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
# Step 6: Train the model
clf = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    min_samples_split=5,
    max_features="sqrt",
    class_weight={0: 1, 1: 1},  # Increase weight for class 0
    random_state=1
)
clf.fit(X_train_smote, y_train_smote)

# Step 7: Evaluate the model
class_distr = {0: 20, 1: 20}  # Adjust as per your need
smote_test = SMOTE(sampling_strategy=class_distr, k_neighbors=1, random_state=123)
X_test_smote, y_test_smote = smote_test.fit_resample(X_test, y_test); y_test_smote = 1 - y_test_smote;
y_pred = clf.predict(X_test_smote)
accuracy = accuracy_score(y_test_smote, y_pred)
roc_auc = roc_auc_score(y_test_smote, clf.predict_proba(X_test_smote)[:, 1])

print(f"Accuracy: {accuracy:.2f}")
print(f"ROC-AUC: {roc_auc:.2f}")
print("\nClassification Report:")
print(classification_report(y_test_smote, y_pred, zero_division=0))

# Create a dictionary to store both
model_data = { 'model': clf, 'feature_names': feature_names, "normalizer": normalizer}
# Save the model for future use
import joblib
joblib.dump(model_data, 'ovarian_rnaseq_model.pkl')
