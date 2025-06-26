from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
)
from sklearn.inspection import permutation_importance

import matplotlib.pyplot as plt
import io
import os 
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

    # Load the model
    with open("prediabetes_proteomics_model.pkl", 'rb') as file:
        model = pickle.load(file)

    # Load dataset
    df = pd.read_csv("augmented_baseline_proteomics.csv")

    # Define features and target
    X = df.drop(columns=["response"])
    y = df["response"]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    y_test_pred = model.predict(X_test)

    cm = confusion_matrix(y_test, y_test_pred)
    cm_plot = CMtoCMDisplay(cm)

    full_importances = permutation_importance(model, X_test, y_test)
    importance = full_importances["importances_mean"]
    feature_names = model.feature_names_in_
    feature_importance = []
    for f in zip(feature_names, importance):
        feature_importance.append((f[0], f[1]))
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    # print(feature_importance)

    with open("metadata.json", "w") as fp:
        json.dump({
            "feature_importance": feature_importance,
            "confusion_matrix": cm_plot,
        },
        fp, indent=2)

