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

###############################################

def get_model_metadata(classifier, labels, training_data):

    return

if __name__ == "__main__":

    # Open the pickle file
    with open("literature_mg_v1.1.pkl", "rb") as fp:
        model = pickle.load(fp)

    # Load dataset
    train_table = pd.read_csv("cleaned_literature_mg_v1.1.csv")
    # Split dataset into training (75%) and testing (25%) set
    X = train_table.drop(["Status", "Reference"], axis=1)
    y = train_table["Status"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=123
    )

    y_pred = model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    cm_plot = CMtoCMDisplay(cm)

    importances = model.feature_importances_
    feature_names = train_table.columns
    
    feature_importance = []
    for item in zip(feature_names, importances):
        feature_importance.append((item[0], item[1]))

    feature_importance.sort(key=lambda x: x[1], reverse=True)

    with open("metadata.json", "w") as fp:
        json.dump({
            "feature_importance": feature_importance,
            "confusion_matrix": cm_plot,
        },
        fp, indent=2)

