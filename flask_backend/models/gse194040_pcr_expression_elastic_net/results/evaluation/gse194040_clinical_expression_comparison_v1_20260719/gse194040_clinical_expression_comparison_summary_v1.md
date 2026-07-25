# GSE194040 clinical and expression model comparison (v1)

Run timestamp: 2026-07-19T22:20:22

## Design

- Clinical baseline and clinical-plus-expression models were tuned and fit using saved training membership only.
- The locked test set was scored once after both specifications and hyperparameter grids were finalized.
- The existing frozen expression-model prediction file was reused without modifying the model or canonical results.
- Calibration intercept and slope are test-set diagnostics only; no calibration mapping was saved or applied.
- Confidence intervals use 2000 paired patient-level percentile replicates with base seed 20260719.

## Selected training-CV models

- Clinical baseline: `{"classifier__C": 0.01, "classifier__penalty": "l2"}`; mean training CV AUC 0.719828.
- Clinical plus expression: `{"classifier__C": 0.03, "classifier__l1_ratio": 0.8}`; mean training CV AUC 0.758801.

## Locked-test results

| Model | ROC AUC (95% CI) | PR-AUC (95% CI) | Brier (95% CI) | Calibration intercept (95% CI) | Calibration slope (95% CI) |
|---|---:|---:|---:|---:|---:|
| clinical_baseline | 0.705 (0.632-0.779) | 0.491 (0.383-0.623) | 0.218 (0.204-0.232) | -0.673 (-1.017--0.370) | 1.678 (1.071-2.503) |
| expression_model_existing | 0.791 (0.724-0.853) | 0.584 (0.471-0.715) | 0.187 (0.165-0.209) | -0.637 (-0.992--0.292) | 1.335 (0.946-1.867) |
| clinical_plus_expression | 0.789 (0.717-0.852) | 0.581 (0.467-0.713) | 0.187 (0.166-0.211) | -0.635 (-0.991--0.293) | 1.324 (0.909-1.864) |

## Paired discrimination differences

Positive values favor model A. Intervals containing zero do not demonstrate a difference on this locked test sample.

| Model A | Model B | Metric | Difference (95% CI) |
|---|---|---|---:|
| clinical_baseline | expression_model_existing | roc_auc | -0.085 (-0.160--0.017) |
| clinical_baseline | expression_model_existing | pr_auc_average_precision | -0.093 (-0.207-0.014) |
| clinical_plus_expression | expression_model_existing | roc_auc | -0.001 (-0.005-0.002) |
| clinical_plus_expression | expression_model_existing | pr_auc_average_precision | -0.002 (-0.012-0.004) |
| clinical_plus_expression | clinical_baseline | roc_auc | 0.084 (0.016-0.158) |
| clinical_plus_expression | clinical_baseline | pr_auc_average_precision | 0.091 (-0.020-0.197) |

All outputs are internal single-split estimates. Model scores remain uncalibrated and must not be interpreted as clinical probabilities. The comparison is not external validation and does not establish clinical utility.
