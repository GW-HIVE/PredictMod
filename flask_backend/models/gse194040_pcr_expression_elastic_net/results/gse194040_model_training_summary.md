# GSE194040 pCR model training summary

Run timestamp: 2026-07-19T18:42:02

## Data and split
- Features: 19134 pretreatment `expr_*` gene-expression columns.
- Target: `pCR` (1 = pathological complete response, 0 = no pCR).
- Training rows: 789; untouched test rows: 198.
- Metadata columns were excluded from features: `sample_id`, `patient_id`, `HR`, `HER2`, `MP`, `treatment_arm`, `gsm`, and `platform`.

## Model selection
- Best model by cross-validated AUC, then F1, then sensitivity: `elastic_net_logistic`.
- Best-model CV AUC: 0.759 +/- 0.026.
- Best-model CV F1: 0.596 +/- 0.033.
- Best-model CV sensitivity: 0.765 +/- 0.035.

## Untouched test performance
- AUC: 0.791
- F1: 0.630
- Sensitivity/recall: 0.719
- Specificity: 0.731
- Precision: 0.561
- Accuracy: 0.727

## Sparse logistic model-selected gene features
- LASSO non-zero genes: 153
- Elastic Net non-zero genes: 211

## Leakage controls and limitations
- Imputation, scaling, supervised feature selection, PCA, and classifier fitting were all inside sklearn pipelines and therefore fit separately within each training fold.
- The final test set was evaluated once after choosing the model from training-set CV.
- This is a single random split of a modest-size high-dimensional cohort; external validation and fold-specific biological stability checks are still needed before interpreting model-selected genes biologically.
- Remaining sparse expression missingness is handled by median imputation inside each training fold or final training pipeline.
