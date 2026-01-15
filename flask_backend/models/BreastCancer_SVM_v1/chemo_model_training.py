
# Breast Cancer Response Prediction (Post-treatment) Combinational Treatment  
# This notebook trains a SVM Classifier to predict patient response based on post-treatment intervention data.

import warnings
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.svm import SVC
from utils import remove_iqr_outliers
from sklearn.model_selection import cross_val_score, KFold
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import GroupShuffleSplit
from argparse import ArgumentParser

warnings.filterwarnings("ignore")

parser = ArgumentParser()
parser.add_argument("--input", type=str, required=True)
args = parser.parse_args()

# Load Data
df = pd.read_csv(args.input)

# Filter for Post_treatment
df_pre_chemo = df[(df['Timeline'] == 'Pre_treatment') & (df['Treatment'] == 'Chemo')].copy()
print(f"Original shape: {df.shape}, Pre-treatment shape: {df_pre_chemo.shape}")

# Drop redundant/irrelevant columns
drop_cols = ['Tissue', 'Identifier', 'Timeline', 'defcls', 'Treatment']
df_chemo = df_pre_chemo.drop(columns=drop_cols)

# Encode categorical variables
le = LabelEncoder()
categorical_cols = ['Response']

label_mappings = {}
for col in categorical_cols:
    df_chemo[col] = le.fit_transform(df_chemo[col])
    label_mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))

#One Hot Encode Origin
categorical_cols = ['Origin']
for col in categorical_cols:
    encoder = OneHotEncoder(sparse_output=False)
    encoded_array = encoder.fit_transform(df_chemo[[col]])
    encoded_df = pd.DataFrame(encoded_array, columns=encoder.get_feature_names_out([col]))
    df_chemo = pd.concat([df_chemo.drop(columns=[col]).reset_index(drop=True), encoded_df], axis=1)

#Outlier Removal

feature_cols = ["Expression", "Origin_breast", "Origin_liver", "nGene",	"percent_mito",	"percent_hsp",	"percent_ig",	"percent_rp",	"nUMI",	"PDCD1"]
label_cols = ["Response"]
df_chemo_ = remove_iqr_outliers(df_chemo, feature_cols)

#Model Training

gss = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=42)

# groups = your patient IDs
groups = df_chemo_["Patient_code"]

train_idx, test_idx = next(gss.split(df_chemo_, df_chemo_["Response"], groups=groups))

train_df = df_chemo_.iloc[train_idx]
test_df  = df_chemo_.iloc[test_idx]

# -------------------------
# Define Model
# -------------------------
def build_model():
    return make_pipeline(
        StandardScaler(),
        SVC(
            kernel="rbf",
            C=15,
            gamma=0.1,
            class_weight="balanced",
            probability=True,
            random_state=42
        )
    )

X = train_df[feature_cols]
y = train_df[label_cols]

kf = KFold(n_splits=3, shuffle=True, random_state=42)

best_auc = -1
best_model = None
fold_num = 1
best_cm = None
# -------------------------
# KFold CV Loop
# -------------------------
for train_idx, val_idx in kf.split(X):

    print(f"\n==============================")
    print(f" Fold {fold_num}")
    print("==============================")

    model = build_model()

    X_tr, X_test = X.iloc[train_idx], X.iloc[val_idx]
    y_tr, y_test = y.iloc[train_idx], y.iloc[val_idx]

    # Train
    model.fit(X_tr, y_tr)

    # Predict
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob) if len(np.unique(y_test)) > 1 else np.nan
    cm = confusion_matrix(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")
    print(f"AUC-ROC: {auc:.4f}")
    print("\nConfusion Matrix:\n", cm)
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # -------------------------
    # SAVE BEST MODEL
    # -------------------------
    if auc > best_auc:   # <-- CHANGE TO acc > best_acc IF YOU WANT ACCURACY
        best_auc = auc
        best_model = model
        best_cm = cm    
        print("🔥 New best model found and stored.")

    fold_num += 1

print("\n==============================")
print(" BEST MODEL FROM CV")
print("==============================")
print(f"Best AUC: {best_auc:.4f}")

#Confusion Matrix

print("\nConfusion Matrix:\n", best_cm)

# -------------------------
# SAVE BEST MODEL TO .pkl
# -------------------------
with open("chemo_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

print("\n✅ Chemo model saved")