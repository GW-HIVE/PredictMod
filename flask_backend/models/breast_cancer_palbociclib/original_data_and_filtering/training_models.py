import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import BorderlineSMOTE, SVMSMOTE
from sklearn.metrics import accuracy_score, roc_auc_score

def test_different_ml_algorithms(file_path):
    # Load dataset
    df = pd.read_csv(file_path, header=None)
    df = df.T 
    # Extract features (X) and labels (y)
    X = df.iloc[1:,1:].values  # All columns except the last one are features
    y = df.iloc[1:,0].astype(int).values   # Last column is the label

    # Split dataset into training and testing sets
    # Check initial class distribution
    # unique, counts = np.unique(y, return_counts=True)
    # print("Class distribution before SMOTE:", dict(zip(unique, counts)))

    # Apply SMOTE to balance the dataset
    # Borderline SMOTE
    smote = BorderlineSMOTE(sampling_strategy={1: 100, 0: 100},kind='borderline-2', k_neighbors=3)
    #smote = SMOTE(sampling_strategy={1: 100, 0: 100},k_neighbors=4,random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Check new class distribution
    unique_resampled, counts_resampled = np.unique(y_resampled, return_counts=True)
    # print("Class distribution after SMOTE:", dict(zip(unique_resampled, counts_resampled)))

    # Split into train/test sets
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define ML models to test
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
        "Support Vector Machine": SVC(kernel="linear", probability=True),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5)
    }

    # Train and evaluate each model
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)  # Train model
        y_pred = model.predict(X_test)  # Predict on test set
        accuracy = accuracy_score(y_test, y_pred)  # Compute accuracy
        roc_score = roc_auc_score(y_test, y_pred)
        results[name] = accuracy
        print(f"{name} Accuracy: {accuracy:.4f}, ROC AUC: {roc_score:.4f}")

    return results

# Run the function with the dataset
file_path = "filtered_C0D0_reduced.csv"  # Update with your actual file path
results = test_different_ml_algorithms(file_path)
