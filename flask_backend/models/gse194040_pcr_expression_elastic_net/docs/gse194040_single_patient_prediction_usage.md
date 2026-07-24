# GSE194040 Single-Patient pCR Prediction

Use `scripts/predict_gse194040_single_patient.py` to score one patient/sample row with the saved Elastic Net pCR model.

## Command

```powershell
python `
  scripts\predict_gse194040_single_patient.py `
  examples\gse194040_single_patient_input_example.csv `
  results\tables\gse194040_single_patient_prediction_example_v2_uncalibrated_score.csv
```

The script loads:

```text
models/gse194040_best_model.joblib
```

## Input Format

The input CSV must contain exactly one row and all `expr_*` gene-expression feature columns used during training. Extra metadata columns are ignored, though `sample_id` and `patient_id` are copied to the output when present.

The target column `pCR` should not be included for real prediction. If present, it is ignored because only `expr_*` model features are used.

## Output Columns

- `sample_id`, when present in input
- `patient_id`, when present in input
- `predicted_pCR_class`: predicted class, where `1` means predicted pCR and `0` means predicted non-pCR
- `predicted_pCR_score`: uncalibrated model score for class `1`
- `predicted_non_pCR_score`: uncalibrated model score for class `0`

These scores are the saved classifier's raw `predict_proba` outputs, renamed to prevent clinical overinterpretation. They are bounded between 0 and 1 and sum to 1, but the model has not undergone probability calibration or external validation. Do not interpret them as clinical probabilities, individualized risks, treatment-response probabilities, or treatment-effect estimates.

The canonical example output is `results/tables/gse194040_single_patient_prediction_example_v2_uncalibrated_score.csv`. Its versioned filename and score-based column names make the uncalibrated status explicit.

## Leakage Note

The saved sklearn pipeline contains the imputer, scaler, and Elastic Net classifier fitted on the final training set only. This prediction script only aligns columns and calls the saved pipeline; it does not refit preprocessing on the input patient.
