#!/usr/bin/env python3
"""Run a single-patient prediction using the saved TCGA-LIHC model bundle."""
import sys
from pathlib import Path
import pandas as pd
import joblib

# Load saved model bundle and the input CSV.
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "best_model_bundle.joblib"
DEFAULT_INPUT = Path(__file__).resolve().parents[1] / "data" / "example_single_patient_input.csv"
input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
bundle = joblib.load(MODEL_PATH)
df = pd.read_csv(input_path)

# Check for missing columns. Extra columns are allowed.
feature_cols = bundle["feature_cols"]
missing = [c for c in feature_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing[:20]}")

# Reorder columns to match training, apply saved preprocessing, and apply saved feature selection.
X = df[feature_cols]
X_proc = bundle["preprocessor"].transform(X)
X_sel = X_proc[:, bundle["selected_idx"]]

# Predict class and probability.
model = bundle["model"]
pred_code = int(model.predict(X_sel)[0])
pred_label = bundle["inverse_label_mapping"][pred_code]
print(f"Prediction: {pred_label}")
if hasattr(model, "predict_proba"):
    print(f"Probability of With Tumor: {model.predict_proba(X_sel)[0, 1]:.3f}")
print(f"Model used: {bundle['model_name']}")
