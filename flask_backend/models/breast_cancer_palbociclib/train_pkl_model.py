import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import BorderlineSMOTE
from sklearn.metrics import accuracy_score, roc_auc_score
import pickle

def test_different_ml_algorithms(file_path):
    # Load dataset
    df = pd.read_csv(file_path, header=None)
    df = df.T 
    # Extract features (X) and labels (y)
    X = df.iloc[1:,1:].values  # All columns except first column and first row
    print(df.iloc[0,1:])
    y = df.iloc[1:,0].astype(int).values   # Last column is the label
    smote = BorderlineSMOTE(sampling_strategy={1: 100, 0: 100},kind='borderline-2', k_neighbors=3)
    #smote = SMOTE(sampling_strategy={1: 100, 0: 100},k_neighbors=4,random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3)
    model = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)
    y_pred = model.predict(X_test)  # Predict on test set
    accuracy = accuracy_score(y_test, y_pred)  # Compute accuracy
    roc_score = roc_auc_score(y_test, y_pred)
    print(f"Forest classifier Accuracy: {accuracy:.4f}, ROC AUC: {roc_score:.4f}")
    with open("trained_model_and_headers.pkl", "wb") as f:
        pickle.dump({"model": model, "feature_headers": df.iloc[0, 1:].tolist()}, f)

# Run the function with the dataset
file_path = "filtered_C0D0_reduced.csv"  # Update with your actual file path
results = test_different_ml_algorithms(file_path)
    