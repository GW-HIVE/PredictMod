# File: methylation_classifier_no_controls.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

# Step 1: Load the data
file_path = 'methyl_data.xlsx'  # Replace with the actual file path
data = pd.read_excel(file_path, header = None)

# Step 2: Extract target (y) from the first row and features (X) from the remaining data
y = data.iloc[0, 1:].values  # First row (excluding the first column) as target vector
y = y.astype(int)
X = data.iloc[1:, 1:].reset_index(drop=True)  # All rows except the first row and first column
X = X.T  # Transpose the matrix
feature_names = data.iloc[1:, 0].values  # First column as feature names

# Step 5: Dimensionality Reduction with PCA
# Initialize PCA - you can specify the number of components (e.g., 5)
pca = PCA(n_components=9)  # Reduce to 5 components, adjust as needed

# Fit PCA and transform the data
X_reduced = pca.fit_transform(X)  # Transpose the DataFrame to have features as rows

# Convert the reduced DataFrame back to pandas format
X_reduced = pd.DataFrame(X_reduced)

# Step 6: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_reduced, y, test_size=0.2, random_state=42
)

# Step 7: Train the model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Step 8: Evaluate the model
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])

print(f"Accuracy: {accuracy:.2f}")
print(f"ROC-AUC: {roc_auc:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the model for future use
import joblib
joblib.dump(clf, 'methylation_model_no_controls.pkl')
