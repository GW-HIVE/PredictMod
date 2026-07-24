# GSE194040 locked held-out evaluation (v2)

Run timestamp: 2026-07-19T21:36:13

## Frozen evaluation design

- Saved model: `models/gse194040_best_model.joblib`
- Saved split: `results/tables/gse194040_train_test_split.csv`
- Held-out patients: 198 (64 pCR; 134 non-pCR).
- The original selected model was loaded without refitting or parameter changes.
- Test outcomes were used only to estimate post-hoc calibration diagnostics.
- No calibration mapping was saved or applied to model outputs.
- Frozen class predictions and model scores were calculated once, then resampled as paired patient-level records.
- Bootstrap: 2000 percentile replicates with NumPy seed 20260719.
- Recomputed AUC and classification metrics matched the canonical metrics CSV before output was written.

## Discrimination and classification

- ROC AUC: 0.790578
- PR-AUC (average precision): 0.583637
- Accuracy: 0.727273
- Sensitivity: 0.718750
- Specificity: 0.731343
- Precision: 0.560976
- F1: 0.630137

## Calibration diagnostics

- Brier score: 0.186545
- Calibration intercept: -0.637415
- Calibration slope: 1.335254
- Mean predicted pCR model score: 0.448139
- Observed held-out pCR rate: 0.323232
- Observed minus predicted rate: -0.124906

The classifier outputs remain uncalibrated model scores. These diagnostics do not convert them into clinical probabilities or establish external validity.

## Outputs

- `gse194040_locked_test_point_metrics_v2.csv`
- `gse194040_locked_test_bootstrap_95ci_v2.csv`
- `gse194040_locked_test_predictions_v2.csv`
- `gse194040_heldout_calibration_metrics_v2.csv`
- `gse194040_heldout_calibration_curve_v2.csv`
- `gse194040_observed_vs_predicted_pcr_rates_v2.csv`
- `gse194040_heldout_calibration_plot_v2.png`
- `gse194040_locked_test_evaluation_session_v2.json`
