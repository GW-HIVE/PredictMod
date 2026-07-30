# Draft BioCompute Object: TCGA-LIHC Tumor-Status Prediction Workflow

**Status:** Draft / unreviewed  
**BCO version:** 0.2.0-draft  
**Object ID:** `urn:uuid:5a9b6074-33c1-4f91-a905-df32badf7da4`  
**Spec version:** `https://w3id.org/biocompute/1.3.0/`  
**Scope:** This BCO documents the model-training workflow beginning with the harmonized TCGA-LIHC ML-ready table, while also recording the upstream public data sources used to create that table.

## 1. Provenance Domain

- **Name:** TCGA-LIHC tumor-status prediction workflow
- **Contributor:** Sri Piramanayagam
- **Review status:** unreviewed; PredictMod mentor review pending
- **Derived from:** PMID 34975338; TCGA-LIHC clinical and RNA-seq data sources
- **Created:** 2026-07-21T16:29:44+00:00
- **Modified:** 2026-07-21T16:29:44+00:00
- **License note:** Draft project documentation. Source data remain governed by TCGA/GDC/UCSC Xena terms. Training package license TBD.

## 2. Usability Domain

This workflow trains a baseline PredictMod-style binary classifier for TCGA-LIHC hepatocellular carcinoma. The model predicts follow-up tumor status, simplified as **Tumor Free vs With Tumor**, using clinical variables and RNA-seq gene-expression features. It is intended as an exploratory tumor-status/prognosis model, not as a direct immunotherapy responder/non-responder model and not as a clinical decision tool.

## 3. Description Domain

### Keywords
TCGA-LIHC; hepatocellular carcinoma; liver cancer; RNA-seq; gene expression; tumor status; Tumor Free; With Tumor; Random Forest; XGBoost; PredictMod; BioCompute Object.

### External references
- PubMed: PMID 34975338
- NCI GDC Project: TCGA-LIHC
- UCSC Xena/GDC Hub: GDC TCGA Liver Cancer (LIHC), STAR FPKM-UQ expression matrix

### Pipeline steps

1. **select_dataset:** selected PMID 34975338 and TCGA-LIHC.
2. **extract_metadata:** downloaded clinical and biospecimen metadata from NCI GDC.
3. **extract_expression:** downloaded STAR FPKM-UQ RNA-seq matrix from UCSC Xena/GDC Hub.
4. **harmonize_table:** matched patient/sample IDs, created Tumor Free/With Tumor labels, excluded missing/unknown labels, and generated the ML-ready table.
5. **split_preprocess:** created X/y, removed ID and label-related columns, used stratified 80/20 split, imputed missing values, scaled numeric variables, and one-hot encoded categorical variables.
6. **select_features:** used Random Forest feature importance to select top 15 features.
7. **train_models:** trained Logistic Regression, Random Forest, XGBoost, SVM, and Decision Tree.
8. **evaluate_models:** evaluated accuracy, AUROC, F1, precision, recall, confusion matrices, and SHAP summary plot.
9. **single_patient_prediction:** saved a script to run predictions for one patient from the saved model bundle.

## 4. Execution Domain

- **Driver:** Python
- **Training script:** `scripts/train_models.py`
- **Single-patient script:** `scripts/single_patient_predict.py`
- **Main packages:** pandas, numpy, scikit-learn, matplotlib, joblib, xgboost, shap, seaborn

## 5. Parametric Domain

- Outcome: Tumor Free=0, With Tumor=1
- Missing/unknown outcome labels: excluded
- Initial gene features: top 500 most variable genes
- Train/test split: 80/20 stratified
- Random seed: 42
- Numeric imputation: median
- Categorical imputation: most frequent
- Numeric scaling: StandardScaler
- Categorical encoding: OneHotEncoder(handle_unknown='ignore')
- Feature selection: RandomForestClassifier, top 15 features
- Models trained: Logistic Regression, Random Forest, XGBoost, SVM, Decision Tree
- Model selection: highest AUROC on held-out test set

## 6. Input and Output Domain

### Inputs
- PMID 34975338 PubMed record
- TCGA-LIHC GDC project page
- TCGA-LIHC clinical metadata
- TCGA-LIHC STAR FPKM-UQ RNA-seq expression matrix
- Derived ML-ready training table

### Outputs
- `results/model_metrics_comparison.csv`
- `results/holdout_predictions_all_models.csv`
- `results/selected_top15_features.csv`
- `results/confusion_matrices.json`
- `models/best_model_bundle.joblib`
- `figures/model_auroc_comparison.png`
- `figures/best_model_confusion_matrix.png`
- `figures/shap_summary_plot.png`
- `scripts/single_patient_predict.py`

## 7. Error Domain / Limitations

### Empirical error
- Best model: Random Forest
- Holdout test set: 71 patients/samples
- Accuracy: 0.8028
- AUROC: 0.7984
- F1 for With Tumor: 0.7586
- Precision for With Tumor: 0.7857
- Recall for With Tumor: 0.7333
- Confusion matrix: `[[35, 6], [8, 22]]`
- External validation: not performed in this draft workflow

### Algorithmic and data limitations
- Tumor Free vs With Tumor is a follow-up tumor-status label, not a controlled direct treatment-response label.
- Missing/unknown tumor-status labels were excluded, which may introduce selection bias.
- The dataset is relatively small for RNA-seq ML: 352 matched labeled samples.
- Feature selection reduces dimensionality but does not eliminate overfitting risk.
- Results may vary if random seed, package versions, model settings, or selected features change.
- The model is exploratory and not for clinical decision-making.
