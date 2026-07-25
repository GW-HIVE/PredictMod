# BCO companion documentation: GSE194040 exploratory pooled pCR classifier

This Markdown file is the human-readable companion to `bco/gse194040_pcr_pipeline_bco_v1.json`. The JSON is the schema-validated IEEE 2791 object; this file is retained for project review and operational context.

## Overview and usability domains

The workflow prepares the public GSE194040/I-SPY2 expression data and applies an exploratory pooled binary classifier for pathological complete response (`pCR`). It supports reproducible research evaluation and validated one-row inference with the frozen scikit-learn pipeline. The submitted frozen artifact is the historical three-step `imputer` → `scaler` → `classifier` pipeline, not a binary produced by the corrected current training script.

It is not a treatment-selection model, does not estimate treatment effects or treatment-arm benefit, and does not output calibrated clinical probabilities or individualized clinical risk. It has one internal locked test split and no external validation.

## Provenance domain

- Source accession: NCBI GEO `GSE194040`.
- Expression input: `GSE194040_ISPY2ResID_AgilentGeneExp_990_FrshFrzn_meanCol_geneLevel_n988.txt.gz`.
- Metadata inputs: `GSE194040-GPL20078_series_matrix.txt.gz` and `GSE194040-GPL30493_series_matrix.txt.gz`.
- The downloaded archives are intentionally excluded and are fetched from
  NCBI GEO by the included preprocessing script.
- Sole package contributor: Rhea Charles, George Washington University HIVE Lab; role: PredictMod Volunteer; email: `riocx1997@gmail.com`; ORCID: none provided. The BCO contribution field uses the schema-supported PAV term `contributedBy`.
- BCO license: CC BY 4.0. This identifies the BCO document license and does not assert a repository software license.
- Submitted trained-model license: CC BY 4.0 under the PredictMod User Guide.
- PredictMod repository source-code license: MIT. Original GSE194040 data remain
  governed separately by NCBI GEO and the original submitters' terms.

The expression data are treated as submitter-normalized, log2-transformed, gene-level, platform-harmonized, and batch-adjusted. Local preprocessing does not repeat normalization, probe collapse, or ComBat correction.

## Execution domain

### Step 1: preprocessing

```powershell
python scripts\preprocess_gse194040.py
```

The script parses GEO inputs, transposes expression to patient rows, extracts `pCR`, `HR`, `HER2`, `MP`, treatment arm, platform, and accession metadata, merges on normalized patient identifiers, and averages the one duplicated cross-platform patient. It retains all 19,134 gene columns. Full-cohort missingness and variance are descriptive QC only; no gene is removed before the locked split.

Historical primary output:
`data_processed/gse194040_ml_ready_pcr_expression.csv` (987 patients, 19,143
columns, 19,134 expression features). The 124.73 MiB CSV is intentionally
excluded and can be recreated from the documented source inputs.

### Step 2: corrected future retraining

```powershell
python scripts\train_gse194040_models.py `
  --split results\tables\gse194040_train_test_split.csv `
  --cv-folds 3 `
  --n-jobs 1 `
  --output-dir results\evaluation\gse194040_retraining_<new_version>
```

The current script reads, but never rewrites, the saved 789/198 train/test membership. Only `expr_*` columns are model features. Its corrected Elastic Net pipeline is `missingness` → `imputer` → `variance` → `scaler` → `classifier`; supervised feature selection or PCA is included for the model families that use those steps. All fitted transformations and estimators are learned within each training fold. Five prespecified model families are compared on training CV, and a future selected model is evaluated on the locked test membership after selection.

The submitted `models/gse194040_best_model.joblib` predates that correction and contains only `imputer` → `scaler` → `classifier`. The corrected current script did not produce that submitted binary. No retraining or replacement was performed because the leakage audit found that the added missingness and variance filters retained all 19,134 features in the historical training data and exact CV folds.

Non-empty output directories are rejected. Future runs write model, metrics, plots, session versions, and convergence status under a new versioned directory. Those future artifacts will use the corrected pipeline. The historical files under `models/`, `results/tables/`, and `results/figures/` remain the submitted canonical artifacts.

Convergence warnings are not globally suppressed. The frozen selected Elastic Net estimator reports 495 fitted iterations against `max_iter=1500`, so its recorded status is `converged_before_max_iter`; this was read from the existing model without refitting.

### Step 3: single-patient inference

```powershell
python scripts\predict_gse194040_single_patient.py input.csv output.csv
```

The CSV must have exactly one patient row, unique columns, and every model-required expression gene. The script loads the historical three-step frozen pipeline, aligns its 19,134 required features, and applies its fitted imputer, scaler, and classifier without retraining. It rejects unsupported formats, zero or multiple rows, duplicate columns, nonnumeric or infinite values, all-missing expression, more than 20% missing expression, and missing required genes. It writes no prediction on validation failure. Successful output contains a predicted class and `predicted_pCR_score`/`predicted_non_pCR_score`, explicitly uncalibrated model scores.

## Parametric domain

- Locked split: `results/tables/gse194040_train_test_split.csv`.
- Random state: 42.
- Training CV folds: 3.
- Search-level parallelism: `--n-jobs`; default 1, with nested Random Forest jobs fixed at 1.
- Training-fold maximum gene missingness: 20%.
- Training-fold variance threshold: `1e-8`.
- Logistic maximum iterations: 1500 for sparse candidates.
- Selected model parameters: `classifier__C=0.03`, `classifier__l1_ratio=0.8`.
- Single-patient maximum missingness: 20% after all required genes are present.

## Input/output and checksums

The JSON BCO includes IEEE-schema `sha1_checksum` values for raw GEO inputs, the
historical excluded ML-ready dataset, locked split, scripts, exact lockfile,
frozen model, canonical metrics, and current example prediction. Included
package files use intended final GitHub `blob/main` URLs; excluded GEO inputs
use their NCBI HTTPS download URLs, and the excluded derived dataset uses a
content-addressed SHA-1 URN. A separate reproducibility manifest records
SHA-256 values for protected included artifacts and the excluded dataset.

Important outputs include:

- `models/gse194040_best_model.joblib`
- `results/tables/gse194040_cv_model_comparison.csv`
- `results/tables/gse194040_final_test_metrics.csv`
- `results/figures/gse194040_final_roc_curve.png`
- `results/figures/gse194040_final_confusion_matrix.png`
- `results/tables/gse194040_single_patient_prediction_example_v2_uncalibrated_score.csv`

## Error domain and verified empirical results

Canonical locked-test point estimates remain unchanged: ROC AUC 0.790578, accuracy 0.727273, sensitivity 0.718750, specificity 0.731343, precision 0.560976, and F1 0.630137. The versioned locked evaluation reports PR-AUC 0.583637 and a bootstrap ROC-AUC 95% interval of 0.728491–0.852047. Held-out diagnostics report Brier score 0.186545, calibration intercept -0.637415, and calibration slope 1.335254. No calibration mapping was fitted or applied.

The main empirical risks are the single internal split, modest sample size, high-dimensional expression space, subgroup instability, and lack of external validation. Algorithmic reproducibility is controlled with exact versions and seeds, but hardware/BLAS differences may still cause small floating-point variation.

## BCO JSON and validation

- IEEE 2791 object: `bco/gse194040_pcr_pipeline_bco_v1.json`
- Official schema snapshot: `schemas/ieee-2791-v1.4/`
- Validator: `scripts/validate_gse194040_bco.py`
- Saved result: `results/validation/gse194040_bco_validation_v1_20260719.json`

The saved validation used JSON Schema Draft 7 through `jsonschema==4.26.0` and returned `valid` with zero errors.
