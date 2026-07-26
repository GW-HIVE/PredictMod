"""
app.py

A small, standalone demo web app for the BRCA disease-free survival (DFS)
recurrence model. This is not part of the PredictMod platform integration
(it does not touch analysis_interface.py or any other shared file), it is
just a simple browser interface for demoing the model on your own machine,
for example at the volunteership symposium, where someone can fill in one
patient's clinical and genomic details and immediately see a prediction.

How to run it:
    pip install flask joblib pandas
    python app.py

Then open http://127.0.0.1:5000 in a browser.
"""
import json
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, render_template, request

APP_DIR = Path(__file__).resolve().parent

# The trained model already lives one directory up, in this same model
# submission's model/ folder (dfs_model.joblib and model_metadata.json are
# also what train_model.py produces and predict_single_patient.py reads).
# Pointing here instead of keeping a second copy inside demo_app/ avoids
# shipping the same ~48 KB binary twice in this pull request.
MODEL_PATH = APP_DIR.parent / "model" / "dfs_model.joblib"
METADATA_PATH = APP_DIR.parent / "model" / "model_metadata.json"

app = Flask(__name__)

# Loaded once at startup, not per-request, so every prediction is fast and we
# are not re-reading these files from disk on every form submission.
model = joblib.load(MODEL_PATH)
with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

NUMERIC_FEATURES = metadata["numeric_features"]
CATEGORICAL_FEATURES = metadata["categorical_features"]
SCREENING_THRESHOLD = metadata["decision_thresholds"]["screening"]["value"]
BALANCED_THRESHOLD = metadata["decision_thresholds"]["balanced"]["value"]

# Age and tumor mutation burden get their own number inputs on the form.
# Every other numeric feature in this dataset is a 0/1 gene mutation flag,
# so those get rendered as checkboxes instead.
GENE_FEATURES = [f for f in NUMERIC_FEATURES if f not in ("AGE", "TMB_NONSYNONYMOUS")]

# The dropdown choices shown for each categorical field. These are the exact
# categories that existed in the training data (see section 3 of
# brca_dfs_model.ipynb), so a user of this demo can only pick a category the
# model actually learned something about, rather than typing in free text
# that might not match anything the model has seen.
CATEGORY_OPTIONS = {
    "AJCC_PATHOLOGIC_TUMOR_STAGE": [
        "Stage I", "Stage IA", "Stage IB", "Stage II", "Stage IIA", "Stage IIB",
        "Stage IIIA", "Stage IIIB", "Stage IIIC", "Stage IV", "Stage X", "[Discrepancy]",
    ],
    "ER_STATUS_BY_IHC": ["Positive", "Negative"],
    "PR_STATUS_BY_IHC": ["Positive", "Negative", "Indeterminate"],
    "IHC_HER2": ["Positive", "Negative", "Equivocal", "Indeterminate"],
    "CANCER_TYPE": ["Breast Cancer", "Breast Sarcoma", "Skin Cancer, Non-Melanoma"],
    "CANCER_TYPE_DETAILED": [
        "Breast Invasive Ductal Carcinoma", "Breast Invasive Lobular Carcinoma",
        "Adenoid Cystic Breast Cancer", "Breast Mixed Ductal and Lobular Carcinoma",
        "Breast Invasive Mixed Mucinous Carcinoma", "Metaplastic Breast Cancer",
        "Breast Invasive Carcinoma, NOS", "Solid Papillary Carcinoma of the Breast",
        "Malignant Phyllodes Tumor of the Breast", "Invasive Breast Carcinoma",
        "Basal Cell Carcinoma", "Paget Disease of the Nipple",
    ],
}


@app.route("/", methods=["GET"])
def home():
    return render_template(
        "index.html",
        gene_features=GENE_FEATURES,
        category_options=CATEGORY_OPTIONS,
        result=None,
        submitted_values={},
    )


@app.route("/predict", methods=["POST"])
def predict():
    form = request.form

    # Build one patient record from the submitted form, in exactly the
    # column layout the model's pipeline expects. The pipeline handles its
    # own imputation, scaling, and one-hot encoding internally, so we just
    # need to hand it a one-row DataFrame with the right raw values.
    patient = {
        "AGE": float(form["AGE"]),
        "TMB_NONSYNONYMOUS": float(form["TMB_NONSYNONYMOUS"]),
    }
    for gene in GENE_FEATURES:
        # Checkboxes only appear in form data when checked, so a missing key
        # means "not mutated" (0).
        patient[gene] = 1 if form.get(gene) == "on" else 0
    for cat_col in CATEGORICAL_FEATURES:
        patient[cat_col] = form[cat_col]

    patient_df = pd.DataFrame([patient])[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    probability = float(model.predict_proba(patient_df)[0, 1])

    result = {
        "probability_pct": f"{probability:.1%}",
        "screening_flag": probability >= SCREENING_THRESHOLD,
        "balanced_flag": probability >= BALANCED_THRESHOLD,
        "screening_threshold_pct": f"{SCREENING_THRESHOLD:.0%}",
        "balanced_threshold_pct": f"{BALANCED_THRESHOLD:.0%}",
    }

    return render_template(
        "index.html",
        gene_features=GENE_FEATURES,
        category_options=CATEGORY_OPTIONS,
        result=result,
        submitted_values=form,
    )


if __name__ == "__main__":
    app.run(debug=True)
