# GSE194040 Preprocessing Leakage Audit

## Finding

The original `preprocess_gse194040.py` calculated feature missingness and population variance using all 987 labeled patients before the train/test split. Although these rules do not use pCR labels, their selected feature set was informed by the locked test covariates and should instead be learned from training data.

The original training pipeline was otherwise correctly structured:

- Median imputation was inside every sklearn pipeline.
- Standardization was inside all models that required scaling.
- Supervised `SelectKBest(f_classif)` was inside the Random Forest and calibrated Linear SVM pipelines.
- PCA was inside the PCA-logistic pipeline.
- Hyperparameter tuning and model fitting occurred inside training-set cross-validation.

Dataset normalization, log2 transformation, gene-level collapsing, and platform/batch adjustment were performed by the GEO data submitters before publication and are not parameters learned by this project from the locked test set.

## Impact Check Before Editing

The current 19,134-feature dataset and saved split were checked at the historical thresholds: missingness greater than 20% and variance at or below `1e-8`.

| Scope | Failing missingness | Failing variance | Maximum missingness | Minimum variance |
|---|---:|---:|---:|---:|
| Full cohort | 0 | 0 | 6.2817% | 0.074928 |
| Saved training set | 0 | 0 | 5.8302% | 0.074767 |
| CV training fold 1 | 0 | 0 | 5.1331% | 0.071076 |
| CV training fold 2 | 0 | 0 | 6.2738% | 0.077398 |
| CV training fold 3 | 0 | 0 | 6.6540% | 0.073395 |

Thus, the historical filters retained every gene, and the corrected filters also retain every gene in the saved training set and each exact CV training fold. The current dataset, CV inputs, and verified results were not affected.

## Correction

`preprocess_gse194040.py` now performs structural preparation and descriptive QC only. It retains every expression feature and does not remove all-expression-missing patients before splitting. Missingness and variance thresholds are recorded only as downstream pipeline settings.

`train_gse194040_models.py` now places transformations in this order:

1. Training-fit missingness filter.
2. Training-fit median imputation.
3. Training-fit variance filter.
4. Standardization where applicable.
5. Supervised feature selection or PCA where applicable.
6. Classifier fitting.

All steps are cloned and fitted independently inside each CV training fold. The corrected script reads the existing saved split rather than regenerating or overwriting it, and defaults to a new protected versioned output directory.

## Retraining Decision

No retraining or new locked-test evaluation was performed because relocating the filters is an identity operation on the current full training set and all CV folds. Re-evaluating the locked test would add no corrected information. The existing trained model and verified performance results remain the authoritative outputs.

If future data or thresholds cause either filter to remove features, run the corrected script with a new versioned `--output-dir`; those outputs must remain separate from the canonical results.

## Versioned Audit Artifacts

- `results/evaluation/gse194040_preprocessing_leakage_audit_v1_20260719/gse194040_preprocessing_filter_impact_v1.json`
- `results/evaluation/gse194040_preprocessing_leakage_audit_v1_20260719/gse194040_preprocessing_leakage_audit_summary_v1.md`
