"""
Breast Cancer Response Prediction - Chemo Pre-treatment
"""

import warnings
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.svm import SVC
from utils import remove_iqr_outliers, apply_iqr_bounds
from argparse import ArgumentParser

warnings.filterwarnings("ignore")

parser = ArgumentParser()
parser.add_argument("--input", type=str, required=True)
args = parser.parse_args()

print("="*70)
print("CHEMO PRE-TREATMENT MODEL TRAINING")
print("="*70)

# ========================================
# 1. LOAD & FILTER DATA
# ========================================
print("\n[1] Loading and filtering data...")
df = pd.read_csv(args.input)

df_pre_chemo = df[(df['Timeline'] == 'Pre_treatment') & (df['Treatment'] == 'Chemo')].copy()
print(f"Original shape: {df.shape}")
print(f"Pre-treatment Chemo shape: {df_pre_chemo.shape}")
print(f"Patients: {df_pre_chemo['Patient_code'].nunique()}")
print(f"Response distribution:\n{df_pre_chemo['Response'].value_counts()}")

# Drop redundant/irrelevant columns
drop_cols = ['Tissue', 'Identifier', 'Timeline', 'defcls', 'Treatment']
if 'group' in df_pre_chemo.columns:
    drop_cols.append('group')
if 'batch' in df_pre_chemo.columns:
    drop_cols.append('batch')
if 'myleiden' in df_pre_chemo.columns:
    drop_cols.append('myleiden')

df_chemo = df_pre_chemo.drop(columns=drop_cols)

# ========================================
# 2. TRAIN/TEST SPLIT
# ========================================
print("\n[2] Splitting train/test by patient...")

gss = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
groups = df_chemo["Patient_code"]

train_idx, test_idx = next(gss.split(df_chemo, df_chemo["Response"], groups=groups))

train_df = df_chemo.iloc[train_idx].copy()
test_df = df_chemo.iloc[test_idx].copy()

# ========================================
# 3. ENCODE RESPONSE (FIT ON TRAIN ONLY)
# ========================================
print("\n[3] Encoding Response variable (fit on train only)...")

response_encoder = LabelEncoder()
train_df['Response'] = response_encoder.fit_transform(train_df['Response'])
test_df['Response'] = response_encoder.transform(test_df['Response'])

# ========================================
# 4. ONE-HOT ENCODE ORIGIN
# FIT ON ALL UNIQUE VALUES (EXCEPTION TO THE RULE)
# ========================================
print("\n[4] One-hot encoding Origin...")

# Get ALL unique Origin values from both train and test
all_origins = pd.concat([train_df['Origin'], test_df['Origin']]).unique().reshape(-1, 1)

# Fit encoder on all possible categories
origin_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
origin_encoder.fit(all_origins)

print(f"Origin categories: {origin_encoder.categories_[0]}")

# Transform both train and test
train_origin_encoded = origin_encoder.transform(train_df[['Origin']])
test_origin_encoded = origin_encoder.transform(test_df[['Origin']])

# Create DataFrames
train_origin_df = pd.DataFrame(
    train_origin_encoded,
    columns=origin_encoder.get_feature_names_out(['Origin']),
    index=train_df.index
)
test_origin_df = pd.DataFrame(
    test_origin_encoded,
    columns=origin_encoder.get_feature_names_out(['Origin']),
    index=test_df.index
)

# Concatenate
train_df = pd.concat([train_df.drop(columns=['Origin']), train_origin_df], axis=1)
test_df = pd.concat([test_df.drop(columns=['Origin']), test_origin_df], axis=1)

print(f"Origin columns created: {list(origin_encoder.get_feature_names_out(['Origin']))}")

# ========================================
# 5. OUTLIER REMOVAL (FIT ON TRAIN ONLY)
# ========================================
print("\n[5] Removing outliers (fit on train only)...")

feature_cols = ["Expression", "Origin_breast", "Origin_liver", "nGene", 
                "percent_mito", "percent_hsp", "percent_ig", "percent_rp", 
                "nUMI", "PDCD1"]

print(f"Train before outlier removal: {len(train_df)} cells")
train_df, iqr_bounds = remove_iqr_outliers(train_df, feature_cols)
print(f"Train after outlier removal: {len(train_df)} cells")

print(f"Test before outlier removal: {len(test_df)} cells")
test_df = apply_iqr_bounds(test_df, iqr_bounds)
print(f"Test after outlier removal: {len(test_df)} cells")

# ========================================
# 6. PREPARE FEATURES
# ========================================
X_train = train_df[feature_cols].values
y_train = train_df['Response'].values
groups_train = train_df['Patient_code'].values

X_test = test_df[feature_cols].values
y_test = test_df['Response'].values

print(f"\n[6] Feature shapes:")
print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
print(f"X_test:  {X_test.shape}, y_test:  {y_test.shape}")

# ========================================
# 7. DEFINE MODEL
# ========================================
def build_model():
    return Pipeline([
        ('scaler', StandardScaler()),
        ('svm', SVC(
            kernel="rbf",
            C=15,
            gamma=0.1,
            class_weight="balanced",
            probability=True,
            random_state=42
        ))
    ])

# ========================================
# 8. CROSS-VALIDATION (GroupKFold)
# ========================================
print("\n[7] Cross-validation with GroupKFold...")

n_patients = train_df['Patient_code'].nunique()
n_folds = min(3, n_patients)
print(f"Using {n_folds}-fold GroupKFold CV")

gkf = GroupKFold(n_splits=n_folds)

cv_results = []
fold_num = 1

for train_idx, val_idx in gkf.split(X_train, y_train, groups_train):
    print(f"\n{'='*50}")
    print(f"Fold {fold_num}/{n_folds}")
    print(f"{'='*50}")

    model = build_model()

    X_tr, X_val = X_train[train_idx], X_train[val_idx]
    y_tr, y_val = y_train[train_idx], y_train[val_idx]

    # Get patient IDs for this fold
    train_pats = train_df.iloc[train_idx]['Patient_code'].unique()
    val_pats = train_df.iloc[val_idx]['Patient_code'].unique()

    print(f"Train patients: {sorted(train_pats)}")
    print(f"Val patients:   {sorted(val_pats)}")
    print(f"Train: {len(X_tr)} cells, Val: {len(X_val)} cells")

    # Train
    model.fit(X_tr, y_tr.ravel())

    # Predict
    y_pred = model.predict(X_val)
    y_prob = model.predict_proba(X_val)[:, 1]

    # Metrics
    acc = accuracy_score(y_val, y_pred)
    auc = roc_auc_score(y_val, y_prob) if len(np.unique(y_val)) > 1 else np.nan
    cm = confusion_matrix(y_val, y_pred)

    print(f"Accuracy: {acc:.4f}")
    print(f"AUC-ROC:  {auc:.4f}")
    print(f"Confusion Matrix:\n{cm}")

    cv_results.append({
        'fold': fold_num,
        'accuracy': acc,
        'auc': auc
    })

    fold_num += 1

# CV Summary
cv_df = pd.DataFrame(cv_results)
print(f"\n{'='*50}")
print("CROSS-VALIDATION SUMMARY")
print(f"{'='*50}")
print(cv_df.to_string(index=False))
print(f"\nMean Accuracy: {cv_df['accuracy'].mean():.4f} ± {cv_df['accuracy'].std():.4f}")
if not cv_df['auc'].isna().all():
    print(f"Mean AUC:      {cv_df['auc'].mean():.4f} ± {cv_df['auc'].std():.4f}")

# ========================================
# 9. TRAIN FINAL MODEL (on full training set)
# ========================================
print(f"\n[8] Training final model on FULL training set...")

final_model = build_model()
final_model.fit(X_train, y_train.ravel())

# ========================================
# 10. EVALUATE ON TEST SET
# ========================================
print(f"\n[9] Evaluating on held-out test set...")

y_test_pred = final_model.predict(X_test)
y_test_prob = final_model.predict_proba(X_test)[:, 1] if len(np.unique(y_test)) > 1 else None

test_acc = accuracy_score(y_test, y_test_pred)
test_auc = roc_auc_score(y_test, y_test_prob) if y_test_prob is not None and len(np.unique(y_test)) > 1 else np.nan
test_cm = confusion_matrix(y_test, y_test_pred)

print(f"\n{'='*50}")
print("TEST SET EVALUATION")
print(f"{'='*50}")
print(f"Accuracy: {test_acc:.4f}")
print(f"AUC-ROC:  {test_auc:.4f}")
print(f"Confusion Matrix:\n{test_cm}")
if len(np.unique(y_test)) > 1:
    print(f"\nClassification Report:\n{classification_report(y_test, y_test_pred, target_names=response_encoder.classes_)}")

# ========================================
# 11. SAVE MODEL & ARTIFACTS
# ========================================
print(f"\n[10] Saving model and preprocessing artifacts...")

model_artifact = {
    'model': final_model,
    'response_encoder': response_encoder,
    'origin_encoder': origin_encoder,
    'iqr_bounds': iqr_bounds,
    'feature_cols': feature_cols,
    'train_patients': sorted(train_df['Patient_code'].unique()),
    'test_patients': sorted(test_df['Patient_code'].unique()),
    'cv_results': cv_df.to_dict('records'),
    'test_metrics': {
        'accuracy': test_acc,
        'auc': test_auc,
        'confusion_matrix': test_cm.tolist()
    }
}

with open("chemo_model.pkl", "wb") as f:
    pickle.dump(model_artifact, f)

print("Chemo model saved to: chemo_model.pkl")
print("\nModel artifact includes:")
print("  - Trained model (with fitted StandardScaler)")
print("  - Response encoder")
print("  - Origin encoder")
print("  - IQR bounds")
print("  - Feature columns")
print("  - CV results")
print("  - Test metrics")

print("\n" + "="*70)
print("TRAINING COMPLETE")
print("="*70)