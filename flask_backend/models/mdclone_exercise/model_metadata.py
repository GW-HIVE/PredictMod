from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
)
from imblearn.over_sampling import RandomOverSampler

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
def get_feature_importance(classifier, feature_names):
    importances = classifier.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    usable_features = []
    features = list(feature_importance_df["Feature"])
    importances = list(feature_importance_df["Importance"])
    for tup in zip(features, importances):
        print(f"--- {len(tup)} ---")
        usable_features.append((tup[0], tup[1]))
    return usable_features

def prepare_training():
    df = pd.read_excel('Exercise_synthetic_curate.xlsx')
    # Extract features (X) and labels (y)
    feature_names = df.columns[:-1]  # Exclude the last column for Y_data
    X_data = df.iloc[:, :-1]  # All columns except the last one for features
    Y_data = df.iloc[:, -1]   # Last column for labels
    print(X_data)
    return X_data, Y_data, feature_names

def get_model_metadata(trained_model, scaler, X_dat, Y_dat):
    # Balance the classes using RandomOverSampler
    ros = RandomOverSampler(random_state=10)
    X_balanced, Y_balanced = ros.fit_resample(X_dat, Y_dat)

    # Normalize the features
    X_scaled = scaler.fit_transform(X_balanced)

    # Split the data into training and testing sets
    Xtrain, Xtest, ytrain, ytest = train_test_split(X_scaled, Y_balanced, test_size=0.4, random_state=10)

    # Make predictions on the testing data
    y_pred = classifier.predict(Xtest)
    accuracy = accuracy_score(ytest, y_pred)

    # Compute Confusion Matrix
    conf_matrix = confusion_matrix(ytest, y_pred)

    return conf_matrix

###############################################

if __name__ == "__main__":

    # Load the trained model, scaler, and feature names
    model_data = joblib.load('Diabetes_EHR_classifier_and_features.pickle')
    classifier = model_data['classifier']
    scaler = model_data['scaler']
    feature_names = model_data['feature_names']

    X_data, Y_data, feature_names = prepare_training()

    cm = get_model_metadata(classifier, scaler, X_data, Y_data)
    cm_plot = CMtoCMDisplay(cm)

    feature_importance = get_feature_importance(classifier, feature_names)

    print(feature_importance)

    with open("metadata.json", "w") as fp:
        json.dump({
            "feature_importance": feature_importance,
            "confusion_matrix": cm_plot,
        },
        fp, indent=2)

