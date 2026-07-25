# GSE194040 preprocessing leakage audit (v1)

The historical preprocessing script calculated gene missingness and variance before the train/test split. This was structurally corrected even though both filters are outcome-independent.

## Current-dataset impact

| Scope | Genes failing missingness >20% | Genes failing variance <=1e-8 | Maximum missingness | Minimum variance |
|---|---:|---:|---:|---:|
| Full cohort (n=987) | 0 | 0 | 0.062817 | 0.074928 |
| Saved training set (n=789) | 0 | 0 | 0.058302 | 0.074767 |
| CV training fold 1 | 0 | 0 | 0.051331 | 0.071076 |
| CV training fold 2 | 0 | 0 | 0.062738 | 0.077398 |
| CV training fold 3 | 0 | 0 | 0.066540 | 0.073395 |

No gene changes eligibility in the corrected training-only implementation. Therefore the pre-split filtering did not affect the current dataset or verified model-selection inputs. The locked test set was not reused for unnecessary retraining, and original results remain canonical.

## Code correction

- `preprocess_gse194040.py` now retains all genes and patients after structural parsing and target-availability checks. Full-cohort missingness and variance values are descriptive QC only.
- Every candidate in `train_gse194040_models.py` now fits missingness filtering, median imputation, and variance filtering inside each CV fold.
- Scaling remains inside applicable pipelines.
- Supervised `SelectKBest` remains inside the Random Forest and calibrated Linear SVM pipelines.
- PCA remains inside the PCA-logistic pipeline.
- Future training uses the saved locked split and writes to a protected versioned directory by default.

No corrected performance table was generated because the current data are unchanged by the relocated filters. If thresholds or data change later, rerun training with a new versioned `--output-dir` and compare the separately saved results.
