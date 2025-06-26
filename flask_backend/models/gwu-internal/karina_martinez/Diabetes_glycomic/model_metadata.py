from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score,
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

from diabetes_classifier import (
    preprocess_data,
    split_data,
    train_test,
)

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
def eval_model(model, X_test, y_test):
    """
    Evaluate model on unseen test set.
    """
    # Predict test set labels and probabilities
    preds = model.predict(X_test)
    pred_proba = model.predict_proba(X_test)

    # Print metrics
    print (f"F1 score: {f1_score(y_test, preds, average='macro'):.3f}")
    print (f"Accuracy: {accuracy_score(y_test, preds):.3f}")
    print (f"AUC: {roc_auc_score(y_test, pred_proba[:,1]):.3f}")

    # Print confusion matrix
    conf_m = confusion_matrix(y_test, preds)
    return conf_m
###############################################

if __name__ == "__main__":

    input_file = pd.read_csv("HG_FinnRisk.txt", sep="\t", decimal=",")
    model = joblib.load("diabetes_classifier.pkl")

    processed_df = preprocess_data(input_file)

    # Split the data
    X, y = split_data(processed_df)
    X_train, X_test, y_train, y_test = train_test(X,y)

    cm = eval_model(model, X_test, y_test)

    cm_plot = CMtoCMDisplay(cm)

    # pipeline_model = model.get_params()
    model_importances = model[2].get_booster().get_score(importance_type="total_cover")

    feature_importance = []
    for feature_name, importance in model_importances.items():
        f_name = "GP" + str(int(feature_name.replace("f", "")) + 1)
        feature_importance.append((f_name, importance))
    
    feature_importance.sort(key=lambda x: x[1], reverse=True)

    with open("metadata.json", "w") as fp:
        json.dump({
            "feature_importance": feature_importance,
            "confusion_matrix": cm_plot,
        },
        fp, indent=2)

