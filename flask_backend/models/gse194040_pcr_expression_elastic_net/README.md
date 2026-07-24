# GSE194040 exploratory pCR expression classifier

This package prepares public GSE194040/I-SPY2 data and applies a frozen Elastic
Net logistic-regression pipeline to predict pathological complete response
(`pCR`) from pretreatment breast-tumor gene expression.

The package is for reproducible research. It has one internal locked test split,
no external validation, and no fitted calibration mapping. It is not a
treatment-selection model, does not estimate treatment effects, and is not
intended for clinical decision-making. Prediction outputs are uncalibrated model
scores rather than clinical probabilities or individualized risks.

## Required submission components

| Component | Path |
|---|---|
| Data dictionaries and preprocessing records | `data_processed/` |
| Model-training script | `scripts/train_gse194040_models.py` |
| Preprocessing script | `scripts/preprocess_gse194040.py` |
| Single-patient prediction script | `scripts/predict_gse194040_single_patient.py` |
| Frozen selected model | `models/gse194040_best_model.joblib` |
| IEEE 2791 BioCompute Object | `bco/gse194040_pcr_pipeline_bco_v1.json` |

## Frozen model provenance

The submitted `gse194040_best_model.joblib` is the historical selected artifact.
It loads as a `sklearn.pipeline.Pipeline` with exactly three fitted steps:
`imputer` → `scaler` → `classifier`. It accepts 19,134 expression features and
has SHA-256
`e3bbccac97c4495dbb8e8c66a8f35921ca6ff20cbb9e0b0671aaf0a00504f9d4`.

The current `scripts/train_gse194040_models.py` is a corrected implementation
for future, versioned retraining. Its Elastic Net pipeline is
`missingness` → `imputer` → `variance` → `scaler` → `classifier`, with those
transformations fitted inside training-only cross-validation folds. That
corrected script did not produce the submitted historical binary. The submitted
model was not retrained or replaced when the script was corrected.

## Source data and intentional exclusions

The source dataset is NCBI Gene Expression Omnibus accession
[`GSE194040`](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE194040),
"I-SPY2-990 mRNA/RPPA Data Resource: mRNA component."

The 124.73 MiB processed training CSV and the downloaded GEO archives are
intentionally excluded from this submission. They can be recreated from the
public GEO record with `scripts/preprocess_gse194040.py`, which downloads
missing inputs and rebuilds the processed table. The exact source filenames,
NCBI download locations, SHA-1 checksums, processing steps, and historical
output checksums are retained in the BCO, preprocessing summary, and
reproducibility manifest. The historical processed table contained 987 patient
rows, 19,143 columns, and 19,134 expression features.

No Git LFS rules are needed for the remaining package files.

## Environment and validation

Use CPython 3.12.13 and the exact lockfile for current prediction, validation,
and automated testing:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-lock.txt
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python scripts\validate_gse194040_bco.py
```

The intentionally excluded historical
`data_processed/gse194040_ml_ready_pcr_expression.csv` was produced in the
preprocessing environment recorded in
`logs/gse194040_session_info.json`: pandas 3.0.1 and NumPy 2.3.5 on CPython
3.12.13. It has not been regenerated under the current lock. The current lock
uses pandas 2.2.2 and NumPy 2.5.1; it is the supported environment for frozen
model prediction and package testing and is also the intended environment for
future versioned runs.

The verified local submission state passes all 41 tests, and the BCO validates
against the included IEEE 2791 v1.4 Draft-07 schema with zero errors.

## Docker

Build and validate the container from this model directory:

```powershell
docker build -t gse194040-pcr-expression:1.0.0 .
docker run --rm gse194040-pcr-expression:1.0.0 python -m pytest -q
docker run --rm gse194040-pcr-expression:1.0.0 `
  python scripts/validate_gse194040_bco.py
```

Run the included example and copy its output to a mounted host directory:

```powershell
docker run --rm `
  -v "${PWD}\docker_output:/output" `
  gse194040-pcr-expression:1.0.0 `
  python scripts/predict_gse194040_single_patient.py `
  examples/gse194040_single_patient_input_example.csv `
  /output/prediction.csv
```

The Dockerfile is provided for reproducibility. A successful local image build
should be recorded before the pull request is opened.

## Run future versioned preprocessing

```powershell
python scripts\preprocess_gse194040.py
```

The script uses local GEO files when present and can download missing public GEO
inputs. A future run under the current lock must write to a new versioned
location and must not be described as the environment that produced the
historical dataset. The recreated final table contains 987 patients, 19,143
columns, and 19,134 expression features.

## Run corrected future retraining

```powershell
python scripts\train_gse194040_models.py `
  --split results\tables\gse194040_train_test_split.csv `
  --cv-folds 3 `
  --n-jobs 1 `
  --output-dir results\evaluation\gse194040_retraining_<new_version>
```

The saved split is immutable. Missingness filtering, imputation, variance
filtering, scaling, supervised feature selection, PCA, and estimation are
learned inside training-only cross-validation pipelines. This command writes a
new versioned model and evaluation; it does not recreate or overwrite the
submitted historical three-step binary.

## Run one-patient inference

```powershell
python scripts\predict_gse194040_single_patient.py `
  examples\gse194040_single_patient_input_example.csv `
  results\tables\prediction_output.csv
```

Input must contain exactly one patient row and all required `expr_*` columns.
Extra metadata columns are ignored. Invalid inputs are rejected before any
prediction file is written.

## Verified internal performance

- Locked test ROC AUC: 0.791
- Locked test PR-AUC: 0.584
- Sensitivity: 0.719
- Specificity: 0.731
- F1: 0.630
- Accuracy: 0.727

These are internal estimates from a single pooled cohort and must not be
presented as external or clinical validation.

## Citation, attribution, and licensing

Citation metadata are in `CITATION.cff`. Rhea Charles is the sole package
contributor, affiliated with George Washington University HIVE Lab, with the
role PredictMod Volunteer and contact email `riocx1997@gmail.com`. No ORCID was
provided. The BCO uses the schema-supported PAV term `contributedBy` rather
than inventing an authorship or curation role. The source dataset is attributed
to NCBI GEO accession `GSE194040`, titled "I-SPY2-990 mRNA/RPPA Data Resource:
mRNA component." The GEO record lists Denise Wolf, Christina Yau, and
Laura van 't Veer as dataset contributors and associate PubMed IDs `35623341`
and `40905691` with the series.

Licence scopes are documented in `LICENSES.md`; third-party materials are
inventoried in `THIRD_PARTY_NOTICES.md`. The upstream
[`GW-HIVE/PredictMod`](https://github.com/GW-HIVE/PredictMod) repository source
code is MIT licensed with `Copyright © 2022 HIVE-Lab`. The submitted trained
model is CC BY 4.0 under the
[PredictMod User Guide](https://hivelab.biochemistry.gwu.edu/predictmod/help),
which states that shared PredictMod models are available under that licence.
The BCO is CC BY 4.0. PredictMod database sets are CC BY 4.0 under the
[HIVE PredictMod website](https://hivelab.biochemistry.gwu.edu/predictmod/);
the corresponding upstream licence text is maintained in
[`LicenseShow.vue`](https://github.com/GW-HIVE/PredictMod/blob/main/vuetify_app/src/views/LicenseShow.vue).

These PredictMod licences do not apply to the original GSE194040 source data.
The original data remain governed by NCBI GEO and the original data submitters'
terms. The source archives are not redistributed in this package.

## Publication checklist

- Confirm IEEE schema redistribution terms.
- Review `PACKAGE_MANIFEST.md` before staging.
