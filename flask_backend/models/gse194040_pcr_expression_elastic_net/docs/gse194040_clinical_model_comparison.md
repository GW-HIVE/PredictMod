# GSE194040 Clinical and Expression Model Comparison

This analysis compares a clinical baseline, the existing expression model, and a clinical-plus-expression model on the same saved GSE194040 split. It is an internal single-split comparison and does not replace or revise the canonical expression-model results.

## Models

### Clinical baseline

- Variables: `HR`, `HER2`, `MP`, and `treatment_arm`.
- Binary variables are imputed within each training fold and standardized.
- Treatment arm is imputed and one-hot encoded within each training fold with unknown-category handling.
- Class-weighted logistic regression is tuned over L1/L2 penalties and `C` values 0.01, 0.1, 1, and 10.

The training-only 3-fold stratified CV selected L2 logistic regression with `C=0.01`:

- Mean CV ROC AUC: 0.719828
- Mean CV PR-AUC (average precision): 0.558122

### Existing expression model

The existing protected locked-test predictions are reused directly. The model is not refit and the canonical model or performance files are not modified.

### Clinical plus expression

The combined model is methodologically feasible because expression and clinical preprocessing can be contained in one pipeline and fitted independently inside every training CV fold. The model uses:

- All 19,134 expression features with fold-specific median imputation and standardization.
- `HR`, `HER2`, and `MP` with fold-specific preprocessing.
- Fold-specific one-hot encoding of treatment arm.
- Class-weighted Elastic Net logistic regression tuned over the same `C` and `l1_ratio` grid used for the original expression candidate.

Training-only CV selected `C=0.03` and `l1_ratio=0.8`:

- Mean CV ROC AUC: 0.758801
- Mean CV PR-AUC (average precision): 0.574776

## Locked-Test Procedure

The saved membership contains 789 training patients and 198 locked test patients, including 64 pCR cases. Pipeline specifications and hyperparameter grids were finalized before test scoring. Both new best estimators were refit on all saved training patients, saved as new versioned models, and used for one locked-test scoring pass.

The existing expression predictions must reproduce all six canonical classification/discrimination metrics within `1e-12` before the comparison proceeds. Test outcomes are used only for final evaluation and diagnostic calibration analysis.

## Locked-Test Results

PR-AUC is average precision. Brier score is lower-is-better. Calibration intercept and slope have ideal values of 0 and 1, respectively. All 95% confidence intervals use 2,000 paired patient-level nonparametric percentile bootstrap replicates with base seed `20260719` and deterministic model-specific seeds.

| Model | ROC AUC (95% CI) | PR-AUC (95% CI) | Brier score (95% CI) | Calibration intercept (95% CI) | Calibration slope (95% CI) |
|---|---:|---:|---:|---:|---:|
| Clinical baseline | 0.705 (0.632–0.779) | 0.491 (0.383–0.623) | 0.218 (0.204–0.232) | -0.673 (-1.017–-0.370) | 1.678 (1.071–2.503) |
| Existing expression model | 0.791 (0.724–0.853) | 0.584 (0.471–0.715) | 0.187 (0.165–0.209) | -0.637 (-0.992–-0.292) | 1.335 (0.946–1.867) |
| Clinical plus expression | 0.789 (0.717–0.852) | 0.581 (0.467–0.713) | 0.187 (0.166–0.211) | -0.635 (-0.991–-0.293) | 1.324 (0.909–1.864) |

Mean predicted pCR scores were 0.474865 for the clinical baseline, 0.448139 for the existing expression model, and 0.447904 for the combined model, compared with an observed pCR rate of 0.323232. These are uncalibrated model scores, not clinical probabilities.

## Paired Discrimination Comparisons

Positive differences favor model A. The intervals resample the same patients for both models.

| Model A | Model B | Metric | Difference, A−B (95% CI) |
|---|---|---|---:|
| Clinical baseline | Existing expression | ROC AUC | -0.085 (-0.160–-0.017) |
| Clinical baseline | Existing expression | PR-AUC | -0.093 (-0.207–0.014) |
| Clinical plus expression | Existing expression | ROC AUC | -0.001 (-0.005–0.002) |
| Clinical plus expression | Existing expression | PR-AUC | -0.002 (-0.012–0.004) |
| Clinical plus expression | Clinical baseline | ROC AUC | 0.084 (0.016–0.158) |
| Clinical plus expression | Clinical baseline | PR-AUC | 0.091 (-0.020–0.197) |

The expression and combined models have nearly identical locked-test discrimination and calibration. Adding the available clinical variables did not produce a detectable improvement over the existing expression model in this test sample. The clinical baseline had lower ROC AUC; its paired ROC AUC difference from the expression model excluded zero, while its PR-AUC difference did not.

## Calibration Limits

Calibration intercept and slope are diagnostic regressions fitted only to summarize held-out behavior. They are not saved or applied as calibration mappings. None of the score fields should be described as clinical probabilities. External validation and prospective clinical-utility assessment remain necessary.

## Reproduce

```powershell
python scripts\train_evaluate_gse194040_clinical_models.py
```

The default output directory is versioned and protected against overwrite:

```text
results/evaluation/gse194040_clinical_expression_comparison_v1_20260719/
```

To repeat the analysis, specify a new versioned `--output-dir` rather than replacing this result.

## Outputs

- `gse194040_clinical_baseline_model_v1.joblib`
- `gse194040_clinical_plus_expression_model_v1.joblib`
- `gse194040_clinical_models_training_cv_results_v1.csv`
- `gse194040_model_comparison_locked_test_predictions_v1.csv`
- `gse194040_model_comparison_locked_test_metrics_v1.csv`
- `gse194040_model_comparison_bootstrap_95ci_v1.csv`
- `gse194040_model_comparison_pairwise_differences_v1.csv`
- `gse194040_model_comparison_calibration_curve_v1.csv`
- `gse194040_model_comparison_calibration_plot_v1.png`
- `gse194040_clinical_expression_comparison_summary_v1.md`
- `gse194040_clinical_expression_comparison_session_v1.json`
