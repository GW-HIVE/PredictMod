# PredictMod TCGA-LIHC Tumor Status Model

Baseline machine-learning package for predicting follow-up tumor status in TCGA-LIHC liver hepatocellular carcinoma patients.

## Project question

Can TCGA-LIHC clinical variables and primary tumor RNA-seq expression features predict whether a patient is **Tumor Free** or **With Tumor** at follow-up?

## Dataset

- **Cancer type:** Liver hepatocellular carcinoma
- **Source cohort:** TCGA-LIHC
- **Clinical/follow-up metadata:** NCI Genomic Data Commons Data Portal
- **RNA-seq expression matrix:** UCSC Xena / GDC Hub, STAR FPKM-UQ
- **Outcome:** `Tumor Free` vs `With Tumor`
- **Rows used for modeling:** 352 matched primary tumor samples
- **Class balance:** 201 Tumor Free, 151 With Tumor

Missing or unknown tumor-status labels were excluded from the model-ready dataset.

## Modeling approach

This package follows the PredictMod tutorial-style workflow:

1. Load model-ready TCGA-LIHC dataset.
2. Define binary outcome column: `outcome_code`.
3. Remove patient/sample IDs and label-related columns from predictors.
4. Split data into stratified 80/20 train/test sets.
5. Impute missing values:
   - numeric: median
   - categorical: most frequent value
6. Scale numeric features.
7. One-hot encode categorical variables.
8. Use Random Forest feature importance for feature selection.
9. Train and compare multiple algorithms.
10. Save metrics, confusion matrices, predictions, figures, and best model bundle.
11. Run a separate single-patient prediction script.

## Models trained

- Logistic Regression
- Random Forest
- XGBoost
- Support Vector Machine
- Decision Tree

## Current best model

Best model selected by AUROC:

| Model | Accuracy | AUROC | F1 With Tumor | Precision With Tumor | Recall With Tumor |
|---|---:|---:|---:|---:|---:|
| Random Forest | 0.803 | 0.798 | 0.759 | 0.786 | 0.733 |

## Repository structure

```text
tcga_lihc_tumor_status/
├── README.md
├── requirements.txt
├── environment.yml
├── .gitignore
├── data/
│   ├── README.md
│   ├── tcga_lihc_tumor_status_ml_ready_top500_genes.csv.gz
│   ├── training_data_review_100_genes.csv
│   └── example_single_patient_input.csv
├── scripts/
│   ├── README.md
│   ├── train_models.py
│   └── single_patient_predict.py
├── models/
│   ├── README.md
│   └── best_model_bundle.joblib
├── results/
│   ├── README.md
│   ├── model_metrics_comparison.csv
│   ├── selected_top15_features.csv
│   ├── rf_feature_importances_all_features.csv
│   ├── holdout_predictions_all_models.csv
│   ├── confusion_matrices.json
│   └── training_status_summary.csv
├── figures/
│   ├── README.md
│   ├── model_auroc_comparison.png
│   ├── best_model_confusion_matrix.png
│   └── shap_summary_plot.png
└── docs/
    ├── tcga_lihc_tumor_status_bco.json
    ├── tcga_lihc_tumor_status_bco.md
    ├── model_card.md
    └── submission_checklist.md
```

## Quick start

Create and activate a Python environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Train all models:

```bash
python scripts/train_models.py
```

Run a single-patient prediction using the included example input:

```bash
python scripts/single_patient_predict.py
```

Run a single-patient prediction using your own CSV:

```bash
python scripts/single_patient_predict.py path/to/your_patient_input.csv
```

## Output files

Running `scripts/train_models.py` creates or updates:

- `models/best_model_bundle.joblib`
- `results/model_metrics_comparison.csv`
- `results/selected_top15_features.csv`
- `results/rf_feature_importances_all_features.csv`
- `results/holdout_predictions_all_models.csv`
- `results/confusion_matrices.json`
- `figures/model_auroc_comparison.png`
- `figures/best_model_confusion_matrix.png`
- `figures/shap_summary_plot.png`

## Main limitation

This is a tumor-status/prognosis model, not a direct controlled immunotherapy responder/non-responder model. The outcome label comes from clinical follow-up tumor status, so it is less standardized than a treatment-response endpoint from a controlled trial.

## Current status

This is a baseline training package. It is ready for review, rerunning, and model improvement. The model package includes a structured BioCompute Object JSON and a human-readable Markdown version. Future work should include leakage auditing, cross-validation with feature selection inside each fold, hyperparameter tuning, gene-symbol mapping, and external validation.
