from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import io
import os 
import pandas as pd
import joblib
import pickle

import json

from base64 import b64encode
from sklearn.metrics import ConfusionMatrixDisplay

from ccrcc_preprocessing import preprocessed_data
from ccrcc_classifier import (
    stratify_risk,
    split_data,
    train_test,
    get_glycoforms,
    )

RANDOM_SEED = 42

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
    ConfusionMatrixDisplay(conf_m).plot()
    return conf_m
###############################################

if __name__ == "__main__":

    model = joblib.load("ccrcc_classifier.pkl")

    df = preprocessed_data()

    # Split glycoform and metadata
    glycoform_df = df.iloc[:,1:10815]

    # Define metadata columns for inclusion-exclusion
    risk_columns = ["vital status",
                    "days to last known disease status",
                    "disease response",
                    "last known disease status",
                    "days to death",
                    "tissue type"]
    target_df = df[risk_columns]

    # Stratify low and high risk based on inclusion-exclusion criteria
    target_df = stratify_risk(target_df)
    
    # Drop rows without risk and normal tissue rows 
    target_df = target_df[(target_df["tissue type"] == "Tumor")&(target_df["risk"].isin(["High","Low"]))]

    # Format glycoform data column headers and join with selected metadata
    glyco_df = get_glycoforms(glycoform_df)
    df_model = target_df[["risk"]].join(glyco_df)
    
    # Split the data
    X, y = split_data(df_model)
    X_train, X_test, y_train, y_test = train_test(X,y)

    cm = eval_model(model, X_test, y_test)
    cm_plot = CMtoCMDisplay(cm)

    with open("metadata.json", "w") as fp:
        json.dump({
            "confusion_matrix": cm_plot,
        },
        fp, indent=2)

