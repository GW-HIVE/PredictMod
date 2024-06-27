"""
File:           ccrcc_classifier.py
Author:         Karina Martinez
Version:        1.0
Description:    The script takes patient data and labels, splits the data into training and testing sets, 
                and trains a linear regression classifier on the training data. 
                Output is a pickle file named 'ccrcc_classifier.pkl'
"""

# Supress warnings
import warnings
warnings.filterwarnings("ignore") 

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from scipy.stats import mannwhitneyu
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectPercentile
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SequentialFeatureSelector
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
        glycosite = gene + "_" + str(glycosylation_site) + "_" + sequence + "_" + glycan
        site_dict[i] = glycosite
    
    df_dict = {}

    for key,value in site_dict.items():
        df_dict[value] = glycoform_df[key]
    
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


def transform_mannwhitneyu(X,y):
    """
    Convert stats.mannwhitneyu() inputs from two independent samples to X and y for compatibility with Pipeline.
    """
    arg1, arg2 = X[y==0], X[y==1]
    f_statistic, p_values = mannwhitneyu(arg1,arg2)
    return f_statistic, p_values


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
            ("select_fdr", SelectPercentile(transform_mannwhitneyu,percentile=0.09)),
            ("scaling", StandardScaler()),
            ("select_features",SequentialFeatureSelector(LogisticRegression(C=0.21,class_weight="balanced",random_state=RANDOM_SEED),direction="backward",scoring="roc_auc",tol=-0.001)),
            ("classify",LogisticRegression(C=0.21,class_weight="balanced",random_state=RANDOM_SEED))
        ]
    )

    model.fit(X_train, y_train)

    eval_model(model, X_test, y_test)

    joblib.dump(model, "ccrcc_classifier.pkl")


if __name__ == "__main__":
    main()