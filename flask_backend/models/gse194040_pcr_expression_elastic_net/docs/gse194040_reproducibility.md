# GSE194040 reproducibility record

## Historical preprocessing environment

The historical `data_processed/gse194040_ml_ready_pcr_expression.csv` was
produced by the preprocessing run recorded in
`logs/gse194040_session_info.json`. That record identifies CPython 3.12.13 on
64-bit Windows, pandas 3.0.1, and NumPy 2.3.5. The processed dataset was not
regenerated during package preparation and is intentionally excluded from the
submission. These versions remain its historical artifact-producing provenance
even though they differ from the current lock. The included preprocessing
script downloads the three public GEO inputs and recreates the table.

## Current prediction and testing environment

The supported environment for loading the frozen model, running prediction,
validating the BCO, and executing the automated tests is CPython 3.12.13 on
64-bit Windows. `requirements.txt` exactly pins direct dependencies,
`requirements-lock.txt` freezes all installed transitive packages, and
`environment.yml` records Python 3.12.13 and pip 25.0.1.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-lock.txt
.\.venv\Scripts\python -m pip check
.\.venv\Scripts\python -m pytest -q
```

The clean verification environment used NumPy 2.5.1, pandas 2.2.2, SciPy 1.18.0, scikit-learn 1.9.0, joblib 1.5.3, matplotlib 3.11.1, pytest 9.1.1, jsonschema 4.26.0, and referencing 0.37.0. No `python_packages` directory was on `sys.path`; all project scripts are independent of that ignored legacy folder.

The current lock is also intended for future versioned preprocessing and
training runs, but it is not claimed to be the environment that produced the
existing processed dataset. The machine and library details, explicit
historical/current environment roles, lockfile SHA-256, checksums for included
canonical artifacts, checksums and dimensions for intentionally excluded
recreatable data, CPU count, and fitted model iteration status are saved in
`results/reproducibility/gse194040_reproducibility_manifest_v1_20260719.json`.

## Warning and convergence policy

The training script no longer installs any global warning filters. Scikit-learn convergence warnings remain visible. Each future versioned training run writes `logs/gse194040_model_convergence_status.json` for every selected model-family estimator and includes the selected model status in its metadata.

The frozen canonical Elastic Net model was inspected without refitting. Its fitted Logistic Regression reports `n_iter_=[495]` with `max_iter=1500`, recorded as `converged_before_max_iter`. The two frozen clinical-comparison estimators are also recorded in the reproducibility manifest.

## CPU/resource policy

`train_gse194040_models.py` and `train_evaluate_gse194040_clinical_models.py` accept `--n-jobs`. They reject zero and values below -1. `GridSearchCV` owns parallelism; the nested Random Forest uses one job, avoiding an unrequested second all-core pool. The default is one job.

## Output protection

The canonical model, split, metrics, and figures are not rewritten. Training and analysis scripts reject non-empty output directories and require a new versioned location for reruns. The files modified during this work were copied first to `backups/20260719_final_repro_bco_verification/`.

## Verification commands and results

- Current submission suite: 41 automated tests.
- BCO validation: `valid`, zero errors; saved at `results/validation/gse194040_bco_validation_v1_20260719.json`.
- Canonical hash audit: all seven included protected SHA-256 values matched.
  The excluded processed table retains its historical SHA-1/SHA-256 values,
  dimensions (987 rows, 19,143 columns, 19,134 expression features), and source
  archive SHA-1 values in the reproducibility manifest and BCO.

The full model was not retrained. This preserves the locked methodology and verified results; the existing estimator’s convergence status was read directly from the saved artifact.
