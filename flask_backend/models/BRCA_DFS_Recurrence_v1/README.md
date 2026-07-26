# Breast Cancer Disease-Free Survival (DFS) Recurrence Prediction

Predicts a breast cancer patient's risk of disease recurrence or progression
using clinical and genomic data from the TCGA-BRCA cohort.

## Data Source

**Cohort:** TCGA Breast Invasive Carcinoma (TCGA-BRCA), TCGA PanCancer Atlas,
downloaded from cBioPortal.

**Reference publication:** The Cancer Genome Atlas Network, "Comprehensive
molecular portraits of human breast tumors," *Nature*, 2012 (PMID 23000897).
The 12-gene mutation panel used here (TP53, PIK3CA, GATA3, CDH1, PTEN,
MAP3K1, MAP2K4, KRAS, KMT2C, ARID1A, RUNX1, ESR1) comes from this paper.

**895 patients**, 97 of whom experienced recurrence or progression
(about 10.8%).

## Files in this folder

```
breast_cancer_ml_eda.csv     Training dataset (895 patients, 23 columns)
brca_dfs_model.ipynb          Full analysis notebook: EDA, data quality
                               review, baseline models, model improvement,
                               threshold selection, and final model save
train_model.py                Model script. Trains and saves the final model
predict_single_patient.py     Single-patient prediction script
example_patient.json          Sample patient record for the script above
model/dfs_model.joblib         The saved, trained scikit-learn pipeline
model/model_metadata.json      Feature schema, thresholds, performance metrics
BCO.json                       BioCompute Object for this model
demo_app/                      Optional: a small standalone Flask app with a
                                 browser form for trying the model by hand.
                                 Not part of the PredictMod platform, does not
                                 touch analysis_interface.py, just a demo
                                 tool. See demo_app/app.py's docstring to run it.
```

## Question this model answers

Given a breast cancer patient's age, tumor stage, hormone receptor status
(ER, PR, HER2), and mutation status across 12 genes recurrently altered in
breast cancer, can we estimate their risk of disease recurrence or
progression?

## Train the model

```bash
pip install pandas numpy scikit-learn imbalanced-learn joblib matplotlib
python train_model.py
```

Reads `breast_cancer_ml_eda.csv`, trains the final pipeline, prints its
performance, and writes `model/dfs_model.joblib` and
`model/model_metadata.json`.

## Run a single-patient prediction

```bash
python predict_single_patient.py --example
```

or with your own patient record (see `example_patient.json` for the
required fields):

```bash
python predict_single_patient.py --input my_patient.json
```

## Modeling approach

- **Target:** `DFS_STATUS` converted to binary, 1 = Recurred/Progressed,
  0 = DiseaseFree.
- **Features:** age, tumor mutation burden, 11 binary gene mutation flags
  (a 12th gene, `KMT2C`, was dropped since it is constant across this
  cohort), AJCC tumor stage, ER/PR/HER2 status, and cancer type/subtype.
- **Preprocessing:** median imputation and scaling for numeric features,
  most-frequent imputation and one-hot encoding for categorical features.
- **Final model:** Logistic Regression with SMOTE oversampling (default
  hyperparameters). Chosen over Random Forest, SVM, and Gradient Boosting
  (each tried with and without SMOTE, and with and without hyperparameter
  tuning) for its clearly better Average Precision, while being simpler and
  more interpretable. Full comparison and reasoning are in
  `brca_dfs_model.ipynb`.

## Algorithm & Model Performance

| Metric | Value |
|---|---|
| Held-out test ROC-AUC | 0.684 |
| Held-out test Average Precision | 0.310 |
| 5-fold CV ROC-AUC (mean +/- std) | 0.637 +/- 0.059 |

Two decision thresholds are saved in `model/model_metadata.json`:

- **Screening (0.50):** recall 0.74, precision 0.17 on the held-out test
  set. Favors catching more true recurrences, at the cost of more false
  alarms. Fits an early-triage use case.
- **Balanced (0.7271):** recall 0.32, precision 0.27, accuracy 0.84. Favors
  fewer false alarms. Chosen using cross-validated predictions on the
  training set only, never the test set.

Hyperparameter tuning via `RandomizedSearchCV` was attempted and did not
exceed the untuned defaults on this dataset size, most likely because there
are only 97 recurrence events for a search procedure to learn from. That is
reported as a genuine finding in the notebook rather than a search that
"failed" and was hidden.

## Intervention & Outcomes

This model does not evaluate any treatment intervention. It estimates the
probability of one outcome, disease recurrence or progression, from a
patient's baseline clinical and genomic profile at diagnosis. The output is
a probability plus a threshold-based flag, not a diagnosis, and should
support, not replace, clinical judgment.

## Known limitations

- **Right-censoring is not modeled.** `DFS_STATUS` is a snapshot of outcome
  status, not a time-to-event variable. A patient marked "DiseaseFree" with
  short follow-up has not been proven cancer-free forever, only cancer-free
  so far. A survival model (for example, Cox proportional hazards) would be
  the statistically correct way to handle this; this classifier does not.
  See section 4 of `brca_dfs_model.ipynb`.
- The gene panel is limited to 12 genes from a 2012 publication and does not
  reflect the full mutational landscape known today.
- The cohort includes a small number of patients whose `CANCER_TYPE` is
  `Breast Sarcoma` or `Skin Cancer, Non-Melanoma` rather than a breast
  carcinoma subtype, a known TCGA-BRCA cohort quirk, not an extraction
  error.
- This model has not been validated on any cohort outside TCGA-BRCA and is
  a research and educational artifact, not a clinical decision-making tool.
