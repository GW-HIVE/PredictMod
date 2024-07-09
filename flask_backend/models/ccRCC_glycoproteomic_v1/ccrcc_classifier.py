"""
File:           ccrcc_classifier.py
Author:         Karina Martinez
Version:        1.1
Description:    The script takes patient data and labels, splits the data into training and testing sets, 
                and trains a multilayer perceptron classifier on the training data. 
                Output is a pickle file named 'ccrcc_classifier.pkl'
"""

# Supress warnings
import warnings
warnings.filterwarnings("ignore") 

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import Lasso
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
import joblib

from ccrcc_preprocessing import preprocessed_data

RANDOM_SEED = 42

def get_glycoforms(glycoform_df):
    """
    Helper function to display gene, glycosylation site, sequence, and glycan composition in header.
    """
    site_dict = {}

    for i in glycoform_df.columns:
        row = i.split("_")
        gene, pep_start, sequence, gly_site, glycan = row[0], int(row[1]), row[2], int(row[4]), row[5]
        glycosylation_site = pep_start + gly_site - 1
    
        glycosite = gene + "_" + str(glycosylation_site) + "_" + glycan

        if glycosite not in site_dict:
            site_dict[glycosite] = [i]

        else:
            site_dict[glycosite].append(i)

    df_dict = {}

    for key,value in site_dict.items():
        df_dict[key] = glycoform_df[value].sum(axis=1)


    return pd.DataFrame(df_dict)


def stratify_risk(target_df):
    """
    Using inclusion-exclusion criteria, function assigns risk to High, Low or NaN.
    """
    # Retype numeric variables to float
    target_df["days to last known disease status"] = target_df["days to last known disease status"].astype("float")
    target_df["days to death"] = target_df["days to death"].astype("float")

    # Set risk to Low, High or NaN
    target_df["risk"] = np.nan
    target_df.loc[(target_df["vital status"] == "Alive")&(target_df["days to last known disease status"]> 1825), "risk"] = "Low"
    target_df.loc[target_df["disease response"]=="PD-Progressive Disease","risk"] = "High"
    target_df.loc[(target_df["disease response"] == "CR-Complete Response")&(target_df["last known disease status"]=="Tumor free"), "risk"] = "Low"
    target_df.loc[target_df["days to death"] < 1825, "risk"] = "High"
    target_df.loc[target_df["days to death"] >= 1825,"risk"] = "Low"

    return target_df


def split_data(df):
    """
    Encode the target labels, split features and target.
    """
    target = "risk"
    le = LabelEncoder()
    df[target] = le.fit_transform(df[target])

    # Split features and target
    X = df.drop(columns=[target]).reset_index(drop=True)
    y = np.array(df[target])

    return X, y


def train_test(X,y):
    """
    Split the train and test sets, reset the index.
    """
    # Divide the data into training (80%) and test (20%)
    X_train, X_test, y_train, y_test = train_test_split(X,y,
                                                        train_size=0.80,
                                                        random_state=RANDOM_SEED,
                                                        stratify=y)

    # Reset the index
    X_train, X_test = X_train.reset_index(drop=True), X_test.reset_index(drop=True)
    return X_train, X_test, y_train, y_test


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


###############################

def main():

    # Get combined data for training using utility function in file ccrcc_preprocessing.py
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

    # Train the model
    model = Pipeline(
        [
            ("scaling", StandardScaler()),
            ("select_features",SelectFromModel(Lasso(random_state=RANDOM_SEED,max_iter=5000,alpha=0.0003))),
            ("classify",MLPClassifier(random_state=RANDOM_SEED, max_iter=2000,solver='adam',hidden_layer_sizes=(100,)))
        ]
    )

    model.fit(X_train, y_train)

    eval_model(model, X_test, y_test)

    joblib.dump(model, "ccrcc_classifier.pkl")


if __name__ == "__main__":
    main()