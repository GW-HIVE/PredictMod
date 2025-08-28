from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
)
from sklearn.preprocessing import LabelEncoder

import matplotlib.pyplot as plt
import io
import pandas as pd
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

def get_model_metadata(classifier, labels, training_data):
    
    train_predictions = classifier.predict(training_data)

    cm = confusion_matrix(labels, train_predictions)
    labels = classifier.feature_names_in_

    cm_plot = CMtoCMDisplay(cm, labels=labels)

    feature_importance = classifier.tree_.compute_feature_importances()
    ordered_importance = []
    for z in zip(labels, feature_importance):
        ordered_importance.append(z)
    ordered_importance.sort(key=lambda x: x[1], reverse=True)
    print(ordered_importance)
    print("="*80)
    print(cm_plot[:81])

    return ordered_importance, cm_plot

if __name__ == "__main__":

    with open("example_1_classifier.pkl", "rb") as fp:
        classifier = pickle.load(fp)
    data = pd.read_csv("example_feature_data.csv")

    encoder = LabelEncoder()
    Y_data = encoder.fit_transform(data["Status"])
    X_data = data.drop(columns=["Status"])

    feature_importance, cm_plot = get_model_metadata(classifier, Y_data, X_data)

    with open("metadata.json", "w") as fp:
        json.dump({
            "feature_importance": feature_importance,
            "confusion_matrix": cm_plot,
        },
        fp, indent=2)

