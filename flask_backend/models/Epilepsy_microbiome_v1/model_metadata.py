from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
)

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
def preprocess_data(self, patient_data, feature_names):
    # See ../../models/Epilepsy_microbiome/{files} for implementation details

    # Check for missing columns in the new data
    missing_cols = set(feature_names) - set(patient_data.columns)
    for c in missing_cols:
        patient_data[c] = 0  # or some other value that makes sense in your context

    # Check for extra columns in the new data
    extra_cols = set(patient_data.columns) - set(feature_names)
    if extra_cols:
        print(
            f"Warning: Found extra columns in the new data that were not in the training data: {extra_cols}"
        )
        patient_data = patient_data.drop(columns=extra_cols)

    # Reorder the columns of the new data
    patient_data_sort = patient_data.reindex(columns=feature_names)
    if not patient_data.equals(patient_data_sort):
        print(
            f"Message: patient data features was sorted to match order of model features"
        )
    return patient_data_sort
###############################################

def get_model_metadata(classifier, labels, training_data):
    
    train_predictions = classifier.predict(training_data)

    cm = confusion_matrix(labels, train_predictions)
    labels = list(classifier.feature_names_in_)

    print(labels)

    cm_plot = CMtoCMDisplay(cm, labels=labels)

    feature_importance = classifier.coef_.tolist()[0]
    print(feature_importance)
    ordered_importance = []
    for z in zip(labels, feature_importance):
        ordered_importance.append(z)
    ordered_importance.sort(key=lambda x: x[1], reverse=True)
    print(ordered_importance)
    print("="*80)
    print(cm_plot[:81])

    return ordered_importance, cm_plot

if __name__ == "__main__":

    classifier_package = joblib.load("Epilepsy_keto_classifier_and_features.pickle")
    classifier = classifier_package["classifier"]
    encoder = classifier_package["encoder"]
    feature_names = classifier_package["feature_names"]

    data = pd.read_excel("epilepsy_keto_data_500.xlsx")

    X_data = data.iloc[:, 2:]
    Y_str_data = data.iloc[:, 1]

    label_encoder = LabelEncoder()
    Y_data = label_encoder.fit_transform(Y_str_data)

    feature_importance, cm_plot = get_model_metadata(classifier, Y_data, X_data)

    with open("metadata.json", "w") as fp:
        json.dump({
            "feature_importance": feature_importance,
            "confusion_matrix": cm_plot,
        },
        fp, indent=2)

