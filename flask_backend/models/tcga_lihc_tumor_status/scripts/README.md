# Scripts

## `train_models.py`

Runs the full baseline modeling workflow:

1. loads the model-ready dataset,
2. defines the binary outcome,
3. splits train/test data,
4. imputes missing values,
5. scales numeric variables,
6. one-hot encodes categorical variables,
7. uses Random Forest feature importance to select the top 15 features,
8. trains Logistic Regression, Random Forest, XGBoost, SVM, and Decision Tree,
9. saves metrics, predictions, confusion matrices, figures, SHAP plot, and the best model bundle.

Run:

```bash
python scripts/train_models.py
```

## `single_patient_predict.py`

Loads the saved model bundle and predicts Tumor Free vs With Tumor for one patient/sample row.

Run with the included example:

```bash
python scripts/single_patient_predict.py
```

Run with your own CSV:

```bash
python scripts/single_patient_predict.py path/to/patient_input.csv
```
