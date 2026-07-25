# GSE194040 Locked Held-Out Evaluation

This analysis evaluates discrimination, classification uncertainty, and calibration of the already selected Elastic Net model on the saved held-out test split. It is a post-hoc diagnostic and does not alter the trained model or the original discrimination and classification results.

## Reproduce

```powershell
python scripts\analyze_gse194040_calibration.py
```

The script reads:

- `models/gse194040_best_model.joblib`
- `data_processed/gse194040_ml_ready_pcr_expression.csv`
- `results/tables/gse194040_train_test_split.csv`

The current default output directory is versioned and protected against overwrite:

```text
results/evaluation/gse194040_locked_test_evaluation_v2_20260719/
```

The original `results/calibration/gse194040_heldout_calibration_v1_20260719/` directory remains unchanged. To perform another run, supply a new versioned directory with `--output-dir`.

## Evaluation Design

- The saved test membership reconstructs 198 patients: 64 pCR and 134 non-pCR.
- The selected model is loaded exactly as saved and is not refit or tuned.
- The raw class-1 `predict_proba` values are analyzed as uncalibrated pCR model scores.
- The frozen model's class predictions and class-1 scores are calculated once.
- Recomputed ROC AUC, accuracy, sensitivity, specificity, precision, and F1 must match the canonical `gse194040_final_test_metrics.csv` values within `1e-12`, or the script fails without saving results.
- PR-AUC is reported as average precision.
- Confidence intervals use a paired patient-level nonparametric bootstrap: each replicate resamples the observed label, frozen class prediction, and frozen score together.
- The default bootstrap uses 2,000 replicates and NumPy random seed `20260719`.
- No model fitting, calibration fitting, threshold selection, or parameter tuning occurs within the bootstrap.
- The diagnostic intercept/slope regression is not saved and is never applied to patient scores.
- The original AUC, threshold, classifications, and performance result files remain unchanged.

## Definitions

- **Brier score:** mean squared error between the binary pCR outcome and the model score; lower is better.
- **Calibration intercept:** intercept from a diagnostic logistic regression of held-out outcomes on the logit of the frozen model score. An ideal value is 0.
- **Calibration slope:** coefficient from that same diagnostic regression. An ideal value is 1.
- **Calibration curve:** observed pCR rate versus mean predicted pCR model score in ten equal-frequency held-out bins.
- **Observed versus predicted rate:** overall and bin-level difference between observed pCR frequency and mean model score.
- **PR-AUC:** average precision, which summarizes precision over recall thresholds using the frozen held-out scores.
- **Bootstrap 95% CI:** 2.5th and 97.5th percentiles of the paired patient-level bootstrap estimates.

## Results

| Diagnostic | Held-out result |
|---|---:|
| Patients | 198 |
| Observed pCR cases | 64 |
| PR-AUC (average precision) | 0.583637 |
| ROC AUC (95% CI) | 0.790578 (0.728491–0.852047) |
| Accuracy (95% CI) | 0.727273 (0.666667–0.787879) |
| Sensitivity (95% CI) | 0.718750 (0.612903–0.830508) |
| Specificity (95% CI) | 0.731343 (0.653839–0.805561) |
| Precision (95% CI) | 0.560976 (0.458321–0.670592) |
| F1 (95% CI) | 0.630137 (0.537313–0.716981) |
| Brier score | 0.186545 |
| Calibration intercept | -0.637415 |
| Calibration slope | 1.335254 |
| Mean predicted pCR model score | 0.448139 |
| Observed pCR rate | 0.323232 |
| Observed minus predicted rate | -0.124906 |

The original ROC AUC and classification point estimates are unchanged. The overall negative observed-minus-predicted difference indicates that the model score is higher on average than the observed pCR rate in this test set. These internal diagnostics do not establish that the scores are clinical probabilities and do not replace external validation.

## Outputs

- `gse194040_locked_test_point_metrics_v2.csv`
- `gse194040_locked_test_bootstrap_95ci_v2.csv`
- `gse194040_locked_test_predictions_v2.csv`
- `gse194040_heldout_calibration_metrics_v2.csv`
- `gse194040_heldout_calibration_curve_v2.csv`
- `gse194040_observed_vs_predicted_pcr_rates_v2.csv`
- `gse194040_heldout_calibration_plot_v2.png`
- `gse194040_locked_test_evaluation_summary_v2.md`
- `gse194040_locked_test_evaluation_session_v2.json`
