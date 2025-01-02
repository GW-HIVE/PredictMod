# File: methylation_classifier_with_smote.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE
import joblib

# Step 1: Load the data
file_path = 'methyl_data_test.xlsx'  # Replace with the actual file path
data = pd.read_excel(file_path, header=None)

# Step 2: Extract target (y) from the first row and features (X) from the remaining data
y = data.iloc[0, 1:].values  # First row (excluding the first column) as target vector
y = y.astype(int)
X = data.iloc[1:, 1:].reset_index(drop=True)  # All rows except the first row and first column
X = X.T  # Transpose the matrix
feature_names = data.iloc[1:, 0].values  # First column as feature names

# Step 4: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=1
)
print(f'X_train.shape: {X_train.shape}')
print(f'X_test.shape: {X_test.shape}')
print(f'y_train.shape: {y_train}')
print(f'y_test: {y_test}')

# Step 5: Apply SMOTE to the training data
desired_class_distribution = {0: 100, 1: 100}  # Adjust as per your need
smote = SMOTE(sampling_strategy=desired_class_distribution, k_neighbors=1, random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
# Step 6: Train the model
clf = RandomForestClassifier(n_estimators=200, max_depth=50, min_samples_split=5, max_features='sqrt', random_state=1)
clf.fit(X_train_smote, y_train_smote)

# Step 7: Evaluate the model
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])

print(f"Accuracy: {accuracy:.2f}")
print(f"ROC-AUC: {roc_auc:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Step 8: Save the model for future use
joblib.dump(clf, 'methylation_model_with_smote.pkl')
