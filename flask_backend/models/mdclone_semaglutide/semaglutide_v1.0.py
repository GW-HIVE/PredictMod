import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib
import numpy as np

# Load the dataset
data = pd.read_csv('semaglutide_processed.csv')

# Separate features and labels
X = data.iloc[:, :-1]  # Features
y = data.iloc[:, -1]   # Target
# Save column headers for future use
column_headers = X.columns.tolist()

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train Decision Tree Classifier
clf = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
clf.fit(X_train, y_train)

# Evaluate model
y_pred = clf.predict(X_test)
y_pred_proba = clf.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"Accuracy: {accuracy:.4f}")
print(f"ROC AUC: {roc_auc:.4f}")

# Visualize response by feature bins (e.g., age deciles)
pd.qcut(data['cohort reference event-age when condition was documented'], q=10).value_counts()
print(y.value_counts(normalize=True))

# Top 5 predictive features
importances = clf.feature_importances_
top5_indices = np.argsort(importances)[-5:][::-1]
top5_features = [column_headers[i] for i in top5_indices]
top5_scores = importances[top5_indices]

print("\nTop 5 Predictive Features:")
for name, score in zip(top5_features, top5_scores):
    print(f"{name}: {score:.4f}")

# Save model, scaler, and column headers
joblib.dump({
    'model': clf,
    'scaler': scaler,
    'columns': column_headers
}, 'decision_tree_model_bundle.pkl')
