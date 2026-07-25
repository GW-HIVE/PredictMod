# GSE194040 held-out calibration analysis (v1)

Run timestamp: 2026-07-19T21:26:11

## Frozen evaluation design

- Saved model: `models/gse194040_best_model.joblib`
- Saved split: `results/tables/gse194040_train_test_split.csv`
- Held-out patients: 198 (64 pCR; 134 non-pCR).
- The original selected model was loaded without refitting or parameter changes.
- Test outcomes were used only to estimate post-hoc calibration diagnostics.
- No calibration mapping was saved or applied to model outputs.

## Calibration diagnostics

- Brier score: 0.186545
- Calibration intercept: -0.637415
- Calibration slope: 1.335254
- Mean predicted pCR model score: 0.448139
- Observed held-out pCR rate: 0.323232
- Observed minus predicted rate: -0.124906

The classifier outputs remain uncalibrated model scores. These diagnostics do not convert them into clinical probabilities or establish external validity.

## Outputs

- `gse194040_heldout_calibration_metrics_v1.csv`
- `gse194040_heldout_calibration_curve_v1.csv`
- `gse194040_observed_vs_predicted_pcr_rates_v1.csv`
- `gse194040_heldout_calibration_plot_v1.png`
- `gse194040_heldout_calibration_session_v1.json`
