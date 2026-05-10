"""
Breast Cancer Response Prediction - Combination Therapy Pre-treatment
"""

import warnings
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
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
print("COMBINATION THERAPY PRE-TREATMENT MODEL - FINAL")
print("="*70)

# ========================================
# 1. LOAD & FILTER DATA
# ========================================
print("\n[1] Loading data...")
df = pd.read_csv(args.input)

df_pre_combo = df[(df['Timeline'] == 'Pre_treatment') & (df['Treatment'] == 'anti-PDL1+Chemo')].copy()
print(f"Filtered to Pre-treatment Combo: {df_pre_combo.shape[0]} cells, {df_pre_combo['Patient_code'].nunique()} patients")

# Drop unnecessary columns
drop_cols = ['Tissue', 'Identifier', 'Timeline', 'defcls', 'Treatment']
for col in ['group', 'batch', 'myleiden']:
    if col in df_pre_combo.columns:
        drop_cols.append(col)

df_combo = df_pre_combo.drop(columns=drop_cols)

# ========================================
# 2. TRAIN/TEST SPLIT BY PATIENT (FIRST!)
# ========================================
print("\n[2] Patient-level train/test split...")

gss = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
groups = df_combo["Patient_code"]

train_idx, test_idx = next(gss.split(df_combo, df_combo["Response"], groups=groups))

train_df = df_combo.iloc[train_idx].copy()
test_df = df_combo.iloc[test_idx].copy()

print(f"Train: {len(train_df)} cells, {train_df['Patient_code'].nunique()} patients {sorted(train_df['Patient_code'].unique())}")
print(f"Test:  {len(test_df)} cells, {test_df['Patient_code'].nunique()} patients {sorted(test_df['Patient_code'].unique())}")

# ========================================
# 3. ENCODE RESPONSE (TRAIN ONLY)
# ========================================
print("\n[3] Encoding Response...")

response_encoder = LabelEncoder()
train_df['Response'] = response_encoder.fit_transform(train_df['Response'])
test_df['Response'] = response_encoder.transform(test_df['Response'])

label_mappings = dict(zip(response_encoder.classes_, response_encoder.transform(response_encoder.classes_)))
print(f"Encoding: {label_mappings}")

# ========================================
# 4. ONE-HOT ENCODE ORIGIN
# ========================================
print("\n[4] One-hot encoding Origin...")

all_origins = pd.concat([train_df['Origin'], test_df['Origin']]).unique().reshape(-1, 1)

origin_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
origin_encoder.fit(all_origins)

train_origin = origin_encoder.transform(train_df[['Origin']])
test_origin = origin_encoder.transform(test_df[['Origin']])

train_origin_df = pd.DataFrame(train_origin, columns=origin_encoder.get_feature_names_out(['Origin']), index=train_df.index)
test_origin_df = pd.DataFrame(test_origin, columns=origin_encoder.get_feature_names_out(['Origin']), index=test_df.index)

train_df = pd.concat([train_df.drop(columns=['Origin']), train_origin_df], axis=1)
test_df = pd.concat([test_df.drop(columns=['Origin']), test_origin_df], axis=1)

print(f"Origin columns: {list(origin_encoder.get_feature_names_out(['Origin']))}")

# ========================================
# 5. OUTLIER REMOVAL (TRAIN ONLY)
# ========================================
print("\n[5] Outlier removal...")

feature_cols = ["Expression", 'Origin_chest_wall', 'Origin_liver', 'Origin_lymph_node',
                "nGene", "percent_mito", "percent_hsp", "percent_ig", "percent_rp", "nUMI", "PDCD1"]

train_df, iqr_bounds = remove_iqr_outliers(train_df, feature_cols)
# test_df = apply_iqr_bounds(test_df, iqr_bounds)

# ========================================
# 6. PREPARE FEATURES
# ========================================
X_train = train_df[feature_cols].values
y_train = train_df['Response'].values

X_test = test_df[feature_cols].values
y_test = test_df['Response'].values

print(f"\n[6] Final shapes: X_train={X_train.shape}, X_test={X_test.shape}")

# ========================================
# 7. CROSS-VALIDATION ASSESSMENT
# ========================================
print("\n[7] Cross-validation assessment...")

n_patients = train_df['Patient_code'].nunique()
print(f"Training patients: {n_patients}")
print(f"Response in train: R={np.sum(y_train)}, NR={len(y_train)-np.sum(y_train)}")

print(f"\n⚠️  DATASET TOO SMALL FOR RELIABLE CROSS-VALIDATION")
print(f"With only {n_patients} training patients, GroupKFold would create")
print(f"validation folds with insufficient samples or single-class data.")
print(f"\nCross-validation SKIPPED (methodologically correct for this dataset size).")
print(f"Model will be evaluated on held-out test set instead.")

# ========================================
# 8. TRAIN MODEL ON FULL TRAINING SET
# ========================================
print(f"\n[8] Training model on full training set...")

model = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC(kernel="rbf", C=15, gamma=0.1, class_weight="balanced", probability=True, random_state=42))
])

model.fit(X_train, y_train.ravel())
print("✅ Model trained")

# ========================================
# 9. TRAIN SET EVALUATION
# ========================================
print(f"\n[9] Training set performance...")

y_train_pred = model.predict(X_train)
y_train_prob = model.predict_proba(X_train)[:, 1]

train_acc = accuracy_score(y_train, y_train_pred)
train_auc = roc_auc_score(y_train, y_train_prob) if len(np.unique(y_train)) > 1 else np.nan

print(f"Train Accuracy: {train_acc:.4f}")
print(f"Train AUC:      {train_auc:.4f}")

# ========================================
# 10. TEST SET EVALUATION
# ========================================
print(f"\n[10] Test set evaluation...")

y_test_pred = model.predict(X_test)
y_test_prob = model.predict_proba(X_test)[:, 1] if len(np.unique(y_test)) > 1 else None

test_acc = accuracy_score(y_test, y_test_pred)
test_auc = roc_auc_score(y_test, y_test_prob) if y_test_prob is not None and len(np.unique(y_test)) > 1 else np.nan
test_cm = confusion_matrix(y_test, y_test_pred)

print(f"\n{'='*50}")
print("TEST SET RESULTS")
print(f"{'='*50}")
print(f"Accuracy: {test_acc:.4f}")
print(f"AUC:      {test_auc:.4f}")
print(f"\nConfusion Matrix:\n{test_cm}")

if len(np.unique(y_test)) > 1:
    print(f"\nClassification Report:\n{classification_report(y_test, y_test_pred, target_names=response_encoder.classes_)}")

# ========================================
# 11. SAVE MODEL
# ========================================
print(f"\n[11] Saving model...")

model_artifact = {
    'model': model,
    'response_encoder': response_encoder,
    'origin_encoder': origin_encoder,
    'iqr_bounds': iqr_bounds,
    'feature_cols': feature_cols,
    'label_mappings': label_mappings,
    'train_patients': sorted(train_df['Patient_code'].unique()),
    'test_patients': sorted(test_df['Patient_code'].unique()),
    'test_metrics': {
        'accuracy': test_acc,
        'auc': test_auc,
        'confusion_matrix': test_cm.tolist()
    },
    'note': 'CV skipped - dataset too small for reliable GroupKFold'
}

with open("combo_model.pkl", "wb") as f:
    pickle.dump(model_artifact, f)

print("combo_model.pkl saved")

print("\n" + "="*70)
print("TRAINING COMPLETE")
print("="*70)
print(f"\nModel Performance:")
print(f"  Train: Acc={train_acc:.3f}, AUC={train_auc:.3f}")
print(f"  Test:  Acc={test_acc:.3f}, AUC={test_auc:.3f}")
print(f"\nLimitation: Only {n_patients} training patients")
print(f"Results are exploratory - larger cohort needed for robust predictions")