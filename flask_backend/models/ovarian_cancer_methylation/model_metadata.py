from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
)
from imblearn.over_sampling import SMOTE

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

    # Load the saved model
    model_data = joblib.load('methylation_model.pkl')
    classifier = model_data["model"]
    feature_names = model_data["feature_names"]

    # Step 1: Load the data
    # XXX - Data here a different than those below
    # patient_input = pd.read_excel('methyl_data.xlsx', header=None)
    # patient_data = patient_input.iloc[1:, 1:].reset_index(drop=True)
    
    # XXX - Data here a different than those above
    # data = pd.read_excel("methyl_data_test.xlsx", header=None)

    # Step 2: Extract target (y) from the first row and features (X) from the remaining data
    # y = data.iloc[0, 1:].values  # First row (excluding the first column) as target vector
    # y = y.astype(int)
    # X = data.iloc[1:, 1:].reset_index(drop=True)  # All rows except the first row and first column
    # X = X.T  # Transpose the matrix
    # feature_names = data.iloc[1:, 0].values  # First column as feature names

    # # Step 4: Train-Test Split
    # X_train, X_test, y_train, y_test = train_test_split(
    #     X, y, test_size=0.5, random_state=1
    # )

    # # Step 5: Apply SMOTE to the training data
    # desired_class_distribution = {0: 100, 1: 100}  # Adjust as per your need
    # smote = SMOTE(sampling_strategy=desired_class_distribution, k_neighbors=1, random_state=42)
    # X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

    # # Step 7: Evaluate the model
    # y_pred = classifier.predict(X_test)

    # cm = confusion_matrix(y_test, y_pred)
    # cm_plot = CMtoCMDisplay(cm)

    feature_importance = []
    for feature in zip(classifier.feature_importances_, feature_names):
        if float(feature[0]) > 0:
            # Ignore millions of features that are "0"
            feature_importance.append((feature[1], feature[0]))

    feature_importance.sort(key=lambda x: x[1], reverse=True)
    print(feature_importance[:10])

    with open("metadata.json", "w") as fp:
        json.dump({
            "feature_importance": feature_importance,
        },
        fp, indent=2)

