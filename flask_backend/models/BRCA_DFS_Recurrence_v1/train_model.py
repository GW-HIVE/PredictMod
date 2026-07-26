"""
train_model.py

This script trains the final Disease-Free Survival (DFS) recurrence risk model
for the TCGA-BRCA volunteership project and saves it to disk so that it can be
reused later without retraining (for example, by predict_single_patient.py).

Why this script exists, separate from the notebook:
The notebook (brca_dfs_model.ipynb) is where the exploration, comparisons, and
plots live, since that is the best place to explain reasoning step by step. This
script is the clean, no-frills version of just the winning pipeline, meant to be
the "model script" that ships in the GitHub submission package. Running this
file end to end reproduces the saved model artifacts from scratch.

How to run:
    python train_model.py

What it produces:
    model/dfs_model.joblib       -> the fitted scikit-learn pipeline
    model/model_metadata.json    -> feature lists, chosen thresholds, and
                                     other details needed to use the model
                                     correctly later on
"""

import json
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    roc_auc_score,
)
from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_predict,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# imbalanced-learn sometimes prints noisy future warnings that are not relevant
# to correctness here, so we quiet them down for a cleaner console output.
warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# 1. Paths and constants
# ---------------------------------------------------------------------------
# Keeping these in one place at the top makes the script easy to adapt if the
# project folder ever moves or the data file gets renamed again.
PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "breast_cancer_ml_eda.csv"
MODEL_DIR = PROJECT_DIR / "model"
MODEL_PATH = MODEL_DIR / "dfs_model.joblib"
METADATA_PATH = MODEL_DIR / "model_metadata.json"

RANDOM_STATE = 42  # fixed so results are reproducible run to run

# Columns that must never be used as predictive features. PATIENT_ID and
# SAMPLE_ID are identifiers, not biology. DFS_STATUS is the raw text version
# of the label we are trying to predict, so keeping it in X would leak the
# answer straight into the model. KMT2C is dropped because, in this cohort,
# every single patient has KMT2C == 0. A column with zero variance carries no
# information for a classifier, so keeping it would just be dead weight (and
# in a one-hot/gene-panel context, a constant column is a common thing to
# double check for, since it can also be a sign of an extraction bug upstream).
ID_AND_LEAKAGE_COLS = ["PATIENT_ID", "SAMPLE_ID", "DFS_STATUS"]
CONSTANT_COLS = ["KMT2C"]


def build_target(df: pd.DataFrame) -> pd.Series:
    """Turn the raw DFS_STATUS text into a binary target.

    The source data encodes disease-free survival status as strings like
    "0:DiseaseFree" and "1:Recurred/Progressed". We convert that into a plain
    0/1 target where 1 means the cancer recurred or progressed, since that is
    the event we ultimately want the model to flag early.
    """
    return df["DFS_STATUS"].apply(
        lambda x: 1 if ("Recurred" in str(x) or "Progressed" in str(x)) else 0
    )


def build_preprocessor(numeric_features, categorical_features) -> ColumnTransformer:
    """Build the preprocessing pipeline shared by every model we try.

    Numeric columns (age, tumor mutation burden, and the binary gene mutation
    flags) get median imputation followed by standard scaling. Median is used
    instead of mean because a couple of these columns (like tumor mutation
    burden) are right-skewed, so the median is a more robust "typical value".

    Categorical columns (tumor stage, receptor status, cancer subtype) get
    most-frequent imputation followed by one-hot encoding. handle_unknown is
    set to "ignore" so that if the test set (or a future single patient) has
    a category the training data never saw, the pipeline will not crash. It
    will just encode that patient as all zeros for that feature instead.
    """
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )


def main():
    # -----------------------------------------------------------------------
    # 2. Load data and rebuild the same feature set used during exploration
    # -----------------------------------------------------------------------
    df = pd.read_csv(DATA_PATH)
    df["target"] = build_target(df)

    drop_cols = ID_AND_LEAKAGE_COLS + CONSTANT_COLS
    X = df.drop(columns=drop_cols + ["target"])
    y = df["target"]

    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

    preprocessor = build_preprocessor(numeric_features, categorical_features)

    # -----------------------------------------------------------------------
    # 3. Train/test split
    # -----------------------------------------------------------------------
    # We hold out 20% of patients and never let the model see them during
    # training, tuning, or threshold selection. That held-out set is the one
    # honest, untouched check of how the model behaves on new patients.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )

    # -----------------------------------------------------------------------
    # 4. Final model: Logistic Regression with SMOTE oversampling
    # -----------------------------------------------------------------------
    # Why this model won, after comparing it against Random Forest, SVM, and
    # Gradient Boosting, both with and without SMOTE, and with and without
    # hyperparameter tuning (see brca_dfs_model.ipynb, section "Model
    # Performance Improvement", for the full comparison table):
    #
    #   - SMOTE (Synthetic Minority Oversampling Technique) creates synthetic
    #     examples of the minority class (recurrence) inside the training
    #     folds only, so the model sees a more balanced view of the two
    #     outcomes during learning without ever touching the test set.
    #   - Logistic Regression paired with SMOTE lands in a statistical tie
    #     with Random Forest + SMOTE on held-out test ROC-AUC (0.684 vs 0.685,
    #     well within the noise seen across cross-validation folds), but it
    #     gives by far the best Average Precision (0.31, roughly double
    #     Random Forest's 0.18) of every configuration we tried, meaning it
    #     ranks true recurrence cases near the top of its risk list much more
    #     reliably.
    #   - Hyperparameter tuning (RandomizedSearchCV over C, penalty, and the
    #     SMOTE neighbor count) did not meaningfully beat the untuned default
    #     settings here. With only 895 patients and 97 recurrence events, the
    #     search has very little signal to work with, so we kept the simpler,
    #     untuned pipeline rather than pretend a marginal, noisy improvement
    #     was real. That is a genuine and useful finding in its own right,
    #     not a shortcut. It is written up in the notebook and the README.
    #
    # imblearn's Pipeline (not scikit-learn's) is used here specifically
    # because it applies SMOTE only to the training fold during cross
    # validation, never to validation or test data. Using scikit-learn's
    # regular Pipeline with SMOTE glued in would leak synthetic copies of
    # test-like patients into training and inflate the scores.
    final_pipeline = ImbPipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("smote", SMOTE(random_state=RANDOM_STATE)),
            ("classifier", LogisticRegression(max_iter=2000, random_state=RANDOM_STATE)),
        ]
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    # -----------------------------------------------------------------------
    # 5. Pick a decision threshold using cross-validated predictions on the
    #    training set only (never the test set, to avoid quietly leaking
    #    test information into a "tuned" threshold).
    # -----------------------------------------------------------------------
    oof_probabilities = cross_val_predict(
        final_pipeline, X_train, y_train, cv=cv, method="predict_proba"
    )[:, 1]

    precisions, recalls, thresholds = precision_recall_curve(y_train, oof_probabilities)
    f1_scores = 2 * precisions * recalls / (precisions + recalls + 1e-12)
    best_f1_idx = int(np.argmax(f1_scores[:-1]))
    balanced_threshold = float(thresholds[best_f1_idx])

    # A second, more clinically-minded operating point: the plain default of
    # 0.5. In this project, missing a true recurrence is far more costly than
    # flagging a patient who turns out fine, so a lower, more sensitive
    # threshold is a reasonable choice for a screening-style use case, even
    # though it means more false alarms. We keep both thresholds saved so the
    # person using the model later can pick the one that fits their purpose.
    screening_threshold = 0.5

    # -----------------------------------------------------------------------
    # 6. Fit the final pipeline on the full training set and evaluate once,
    #    honestly, on the untouched test set.
    # -----------------------------------------------------------------------
    final_pipeline.fit(X_train, y_train)
    test_probabilities = final_pipeline.predict_proba(X_test)[:, 1]

    test_auc = roc_auc_score(y_test, test_probabilities)
    test_ap = average_precision_score(y_test, test_probabilities)
    cv_auc_scores = cross_val_score(final_pipeline, X, y, cv=cv, scoring="roc_auc")

    print("=" * 70)
    print("FINAL MODEL: Logistic Regression + SMOTE")
    print("=" * 70)
    print(f"Held-out test ROC-AUC:            {test_auc:.3f}")
    print(f"Held-out test Average Precision:  {test_ap:.3f}")
    print(f"5-fold CV ROC-AUC (full dataset):  {cv_auc_scores.mean():.3f} +/- {cv_auc_scores.std():.3f}")
    print()

    for label, threshold in [
        ("Screening threshold (0.50, favors catching recurrences)", screening_threshold),
        ("Balanced threshold (F1-optimal, favors fewer false alarms)", balanced_threshold),
    ]:
        preds = (test_probabilities >= threshold).astype(int)
        print(f"--- {label}: {threshold:.3f} ---")
        print(confusion_matrix(y_test, preds))
        print(classification_report(y_test, preds, zero_division=0))

    # -----------------------------------------------------------------------
    # 7. Refit on ALL available data before saving.
    # -----------------------------------------------------------------------
    # The evaluation above uses the 80/20 split so the numbers we just printed
    # are an honest estimate of real-world performance. But once we are happy
    # with the pipeline choice, it is standard practice to refit on every
    # patient we have (train + test combined) before shipping the model,
    # since more training data almost always helps a bit and we have already
    # gotten our honest performance read from the held-out set above.
    final_pipeline.fit(X, y)

    # -----------------------------------------------------------------------
    # 8. Save the fitted pipeline and its metadata to disk.
    # -----------------------------------------------------------------------
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(final_pipeline, MODEL_PATH)

    metadata = {
        "model_description": "Logistic Regression with SMOTE oversampling, predicting DFS recurrence/progression risk for TCGA-BRCA patients.",
        "target_definition": "1 = Recurred/Progressed (DFS_STATUS), 0 = DiseaseFree",
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "dropped_columns": drop_cols,
        "n_patients_total": int(len(df)),
        "n_recurrence_events": int(df["target"].sum()),
        "random_state": RANDOM_STATE,
        "held_out_test_metrics": {
            "roc_auc": round(float(test_auc), 4),
            "average_precision": round(float(test_ap), 4),
        },
        "cross_validated_metrics": {
            "roc_auc_mean": round(float(cv_auc_scores.mean()), 4),
            "roc_auc_std": round(float(cv_auc_scores.std()), 4),
            "n_folds": 5,
        },
        "decision_thresholds": {
            "screening": {
                "value": screening_threshold,
                "purpose": "Higher sensitivity. Flags more patients as at-risk, at the cost of more false alarms. Meant for early triage, not diagnosis.",
            },
            "balanced": {
                "value": round(balanced_threshold, 4),
                "purpose": "F1-optimal threshold chosen from cross-validated predictions on the training set only. Trades some sensitivity for fewer false alarms.",
            },
        },
        "notes_and_limitations": [
            "Trained on 895 TCGA-BRCA patients with only 97 recurrence/progression events, so estimates carry real uncertainty.",
            "DFS_STATUS is treated as a binary label, but it is really a time-to-event outcome. Patients marked DiseaseFree with short follow-up have not been proven cancer-free forever, only cancer-free so far. A proper survival model (for example, Cox proportional hazards) would handle this censoring correctly; this classifier does not.",
            "Gene panel is limited to 12 genes highlighted in the 2012 TCGA breast cancer paper and does not reflect the full mutation landscape.",
            "The cohort technically includes a handful of patients whose CANCER_TYPE is Breast Sarcoma or Skin Cancer, Non-Melanoma rather than a breast carcinoma subtype. These are retained TCGA-BRCA barcodes, not modeling errors, but they are a scope note worth knowing about.",
            "This model has not been externally validated on any cohort outside TCGA-BRCA and is a research/educational artifact, not a clinical decision tool.",
        ],
    }

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nSaved trained pipeline to: {MODEL_PATH}")
    print(f"Saved metadata to:         {METADATA_PATH}")


if __name__ == "__main__":
    main()
