"""
File:           diabetes_classifier.py
Author:         Karina Martinez
Version:        1.1
Description:    The script takes patient data and labels, splits the data into training 
                and testing sets, and trains an XGBoost classifier on the training data. 
                Output is a pickle file named 'diabetes_classifier.pkl'
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer
from sklearn.feature_selection import SequentialFeatureSelector
import xgboost as xgb
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
import joblib

RANDOM_SEED = 42

def preprocess_data(df):
    """
    Data cleaning function to remove unused columns and consolidate like features.
    """
    # Drop unused columns
    df = df.drop(columns=["Cohort","Sample","BL_AGE","DIAB_AGE","PREVAL_DIAB","INCIDENT_DIAB","DIAB_T2","INCIDENT_DIAB_T2","PREVAL_DIAB_T2","LB","HB","S0","S1","S2","S3","S4","G0","G1","G2","G3","G4"])

    # Add GlyTouCan (https://glytoucan.org/) accessions to glycan peak (GP) headers
    headers = pd.read_csv("gtc_headers.csv", sep=",")
    header_list = df.columns[:1].to_list()
    header_list += headers["Header"].to_list()
    df.columns=header_list

    # Combine features with same structure
    glycan_dict = {
        "GP32-33_G67579EM":["GP32_G67579EM","GP33_G67579EM"],
        "GP38-39_G12638YK":["GP38_G12638YK","GP39_G12638YK"],
        "GP41-43_G16933RK":["GP41_G16933RK","GP42_G16933RK","GP43_G16933RK"]
               }
    
    # Create dataframe with combined features
    df_combined = pd.DataFrame()
    for key,value in glycan_dict.items():
        df_combined[key] = df[value].sum(axis=1)

    # Join combined features with original dataframe, drop individual peaks included in combined features
    df_out = df.join(df_combined)
    df_out = df_out.drop(columns=["GP32_G67579EM","GP33_G67579EM","GP38_G12638YK","GP39_G12638YK","GP41_G16933RK","GP42_G16933RK","GP43_G16933RK"])
    
    return df_out

def split_data(df):
    """
    Encode the target labels, split features and target.
    """
    target = "DIABETES"

    # Encode categorical target in the combined data
    le = LabelEncoder()
    df[target] = le.fit_transform(df[target])

    # Split the data into X and y
    X= df.drop(columns=[target])
    y = np.array(df[target])
    return X,y

def train_test(X,y):
    """
    Split the train and test sets, reset the index.
    """
    # Divide the data into training (80%) and test (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
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

    # Get input data for training
    input_file = pd.read_csv("HG_FinnRisk.txt", sep="\t", decimal=",")

    # Preprocess input data
    processed_df = preprocess_data(input_file)

    # Split the data
    X, y = split_data(processed_df)
    X_train, X_test, y_train, y_test = train_test(X,y)

    # Train the model
    model = Pipeline(
        [
            ("scaling", PowerTransformer()),
            ("select_features",SequentialFeatureSelector(xgb.XGBClassifier(),direction="backward",scoring="roc_auc",tol=0.0001)),
            ("classify", xgb.XGBClassifier(gamma=3, min_child_weight=5))
            ])
    
    model.fit(X_train, y_train)

    eval_model(model, X_test, y_test)

    joblib.dump(model, "diabetes_classifier.pkl")
    

if __name__ == "__main__":
    main()
