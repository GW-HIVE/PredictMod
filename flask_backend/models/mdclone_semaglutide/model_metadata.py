from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

import matplotlib.pyplot as plt
import io
import numpy as np
import pandas as pd
import joblib
import pickle

import json

from base64 import b64encode
from sklearn.metrics import ConfusionMatrixDisplay

def CMtoCMDisplay(cm, labels=None):
    buf = io.BytesIO()
    if labels is not None:
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot()
        plt.savefig(buf, format="png", bbox_inches="tight")
        return b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot()
    plt.savefig(buf, format="png", bbox_inches="tight")
    return b64encode(buf.getvalue()).decode("utf-8").replace("\n", "")

#################### XXX ######################

###############################################

def get_model_metadata(classifier, labels, training_data):

    return

if __name__ == "__main__":

    # Load the dataset
    data = pd.read_csv('semaglutide_processed.csv')

    model_bundle = joblib.load("decision_tree_model_bundle.pkl")

    # Extract classifier, scaler, and feature names
    classifier = model_bundle['model']
    scaler = model_bundle['scaler']
    feature_names = model_bundle['columns']

    # Separate features and labels
    X = data.iloc[:, :-1]  # Features
    y = data.iloc[:, -1]   # Target
    # Save column headers for future use
    column_headers = X.columns.tolist()

    # Normalize features
    X_scaled = scaler.fit_transform(X)

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Evaluate model
    y_pred = classifier.predict(X_test)
    y_pred_proba = classifier.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"ROC AUC: {roc_auc:.4f}")


    cm = confusion_matrix(y_test, y_pred)
    cm_plot = CMtoCMDisplay(cm)

    # Top 5 predictive features
    importances = classifier.feature_importances_
    top5_indices = np.argsort(importances)[-5:][::-1]
    top5_features = [column_headers[i] for i in top5_indices]
    top5_scores = importances[top5_indices]

    feature_importance = []
    for name, score in zip(top5_features, top5_scores):
        feature_importance.append((name, f"{score:.4f}"))

    with open("metadata.json", "w") as fp:
        json.dump({
            "feature_importance": feature_importance,
            "confusion_matrix": cm_plot,
        },
        fp, indent=2)

