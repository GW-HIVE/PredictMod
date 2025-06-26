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

    # Step 1: Load the pickled model
    with open('svm_classifier.pkl', 'rb') as f:
        svm_model = pickle.load(f)

    # print(svm_model.coef_)
    # print(svm_model.ranking_)

    with open("metadata.json", "w") as fp:
        json.dump({
            "feature_importance": "Unavailable in SVM with non-linear kernel",
        },
        fp, indent=2)

