#!/usr/bin/env python3
"""Train TCGA-LIHC tumor-status models. Outcome: outcome_code where 0=Tumor Free and 1=With Tumor."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score, precision_score, recall_score, confusion_matrix
from xgboost import XGBClassifier
import shap

RANDOM_STATE = 42
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "tcga_lihc_tumor_status_ml_ready_top500_genes.csv.gz"
RESULTS = ROOT / "results"
MODELS = ROOT / "models"
FIGURES = ROOT / "figures"
for folder in [RESULTS, MODELS, FIGURES]:
    folder.mkdir(exist_ok=True)

def main():
    # Load ML-ready dataset.
    df = pd.read_csv(DATA_PATH)

    # Remove identifiers and label-related columns from predictors to avoid leakage.
    id_or_label_cols = ["patient_id", "sample_id", "tumor_status", "outcome_code", "label_followup_day"]
    feature_cols = [c for c in df.columns if c not in id_or_label_cols]
    gene_features = [c for c in feature_cols if str(c).startswith("ENSG")]
    clinical_features = [c for c in feature_cols if c not in gene_features]

    # Define X predictors and y binary label.
    X = df[feature_cols].copy()
    y = df["outcome_code"].astype(int)

    # Split into train/test while preserving class balance.
    X_train, X_test, y_train, y_test, train_idx, test_idx = train_test_split(
        X, y, np.arange(len(X)), test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )

    # Median-impute and scale numeric values; mode-impute and one-hot encode categorical values.
    numeric_cols = [c for c in ["age_at_index"] if c in X.columns] + gene_features
    categorical_cols = [c for c in clinical_features if c not in numeric_cols]
    try:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
    preprocessor = ColumnTransformer([
        ("numeric", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_cols),
        ("categorical", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", ohe)]), categorical_cols),
    ], remainder="drop")
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)
    cat_names = list(preprocessor.named_transformers_["categorical"].named_steps["onehot"].get_feature_names_out(categorical_cols)) if categorical_cols else []
    feature_names = np.array(numeric_cols + cat_names)

    # Feature selection using Random Forest importance; keep top 15.
    selector = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, class_weight="balanced", n_jobs=1)
    selector.fit(X_train_proc, y_train)
    importances = selector.feature_importances_
    top_k = 15
    selected_idx = np.argsort(importances)[::-1][:top_k]
    selected_features = feature_names[selected_idx]
    X_train_selected = X_train_proc[:, selected_idx]
    X_test_selected = X_test_proc[:, selected_idx]
    pd.DataFrame({"feature": feature_names, "rf_importance": importances}).sort_values("rf_importance", ascending=False).to_csv(RESULTS / "rf_feature_importances_all_features.csv", index=False)
    pd.DataFrame({"selected_feature": selected_features, "rf_importance": importances[selected_idx]}).to_csv(RESULTS / "selected_top15_features.csv", index=False)

    # Train recommended algorithms: LOGR, RF, XGB; include SVM and DTC as additional comparisons.
    n_pos = int((y_train == 1).sum())
    n_neg = int((y_train == 0).sum())
    scale_pos_weight = n_neg / n_pos if n_pos else 1
    models = {
        "Logistic Regression": LogisticRegression(max_iter=3000, class_weight="balanced", random_state=RANDOM_STATE),
        "Random Forest": RandomForestClassifier(n_estimators=120, min_samples_leaf=3, class_weight="balanced", random_state=RANDOM_STATE, n_jobs=1),
        "XGBoost": XGBClassifier(n_estimators=80, max_depth=3, learning_rate=0.05, subsample=0.85, colsample_bytree=0.85, reg_lambda=1.0, objective="binary:logistic", eval_metric="logloss", tree_method="hist", random_state=RANDOM_STATE, n_jobs=1, scale_pos_weight=scale_pos_weight),
        "SVM": SVC(kernel="rbf", probability=True, class_weight="balanced", random_state=RANDOM_STATE),
        "Decision Tree": DecisionTreeClassifier(max_depth=4, min_samples_leaf=5, class_weight="balanced", random_state=RANDOM_STATE),
    }
    rows, trained_models, confusion_matrices, predictions = [], {}, {}, []
    for name, model in models.items():
        model.fit(X_train_selected, y_train)
        trained_models[name] = model
        pred = model.predict(X_test_selected)
        prob = model.predict_proba(X_test_selected)[:, 1]
        cm = confusion_matrix(y_test, pred, labels=[0, 1])
        confusion_matrices[name] = cm.tolist()
        rows.append({
            "model": name,
            "accuracy": accuracy_score(y_test, pred),
            "auroc": roc_auc_score(y_test, prob),
            "f1_with_tumor": f1_score(y_test, pred, pos_label=1, zero_division=0),
            "precision_with_tumor": precision_score(y_test, pred, pos_label=1, zero_division=0),
            "recall_with_tumor": recall_score(y_test, pred, pos_label=1, zero_division=0),
            "tn_tumor_free_correct": int(cm[0, 0]),
            "fp_pred_with_tumor_when_tumor_free": int(cm[0, 1]),
            "fn_pred_tumor_free_when_with_tumor": int(cm[1, 0]),
            "tp_with_tumor_correct": int(cm[1, 1]),
            "n_train": len(y_train), "n_test": len(y_test), "n_selected_features": top_k,
        })
        predictions.append(pd.DataFrame({
            "patient_id": df.iloc[test_idx]["patient_id"].values,
            "sample_id": df.iloc[test_idx]["sample_id"].values,
            "true_label": pd.Series(y_test).map({0: "Tumor Free", 1: "With Tumor"}).values,
            "predicted_label": pd.Series(pred).map({0: "Tumor Free", 1: "With Tumor"}).values,
            "probability_with_tumor": prob,
            "model": name,
        }))

    # Save metrics, confusion matrices, and holdout predictions.
    metrics = pd.DataFrame(rows).sort_values(["auroc", "f1_with_tumor", "accuracy"], ascending=False)
    metrics.to_csv(RESULTS / "model_metrics_comparison.csv", index=False)
    pd.concat(predictions, ignore_index=True).to_csv(RESULTS / "holdout_predictions_all_models.csv", index=False)
    with open(RESULTS / "confusion_matrices.json", "w") as f:
        json.dump(confusion_matrices, f, indent=2)

    # Save best model by AUROC with preprocessing objects and feature names.
    best_name = metrics.iloc[0]["model"]
    best_model = trained_models[best_name]
    joblib.dump({"preprocessor": preprocessor, "selected_idx": selected_idx, "selected_features": selected_features.tolist(), "model": best_model, "model_name": best_name, "feature_cols": feature_cols, "label_mapping": {"Tumor Free": 0, "With Tumor": 1}, "inverse_label_mapping": {0: "Tumor Free", 1: "With Tumor"}}, MODELS / "best_model_bundle.joblib")
    X_test.iloc[[0]].to_csv(ROOT / "data" / "example_single_patient_input.csv", index=False)

    # Create comparison plots and SHAP plot.
    plot_df = metrics.sort_values("auroc")
    plt.figure(figsize=(8, 4.2)); plt.barh(plot_df["model"], plot_df["auroc"]); plt.xlim(0, 1); plt.xlabel("AUROC"); plt.title("Model comparison by AUROC"); plt.tight_layout(); plt.savefig(FIGURES / "model_auroc_comparison.png", dpi=220); plt.close()
    best_cm = np.array(confusion_matrices[best_name])
    plt.figure(figsize=(4.8, 4.2)); plt.imshow(best_cm); plt.title(f"{best_name} confusion matrix"); plt.xticks([0, 1], ["Pred Tumor Free", "Pred With Tumor"], rotation=20, ha="right"); plt.yticks([0, 1], ["True Tumor Free", "True With Tumor"])
    for i in range(2):
        for j in range(2): plt.text(j, i, str(best_cm[i, j]), ha="center", va="center", fontsize=14)
    plt.tight_layout(); plt.savefig(FIGURES / "best_model_confusion_matrix.png", dpi=220); plt.close()
    X_test_selected_df = pd.DataFrame(X_test_selected, columns=selected_features)
    explainer = shap.TreeExplainer(trained_models["XGBoost"])
    shap_values = explainer.shap_values(X_test_selected_df)
    if isinstance(shap_values, list): shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]
    elif hasattr(shap_values, "ndim") and shap_values.ndim == 3: shap_values = shap_values[:, :, 1]
    shap.summary_plot(shap_values, X_test_selected_df, show=False, max_display=15)
    plt.tight_layout(); plt.savefig(FIGURES / "shap_summary_plot.png", dpi=220, bbox_inches="tight"); plt.close()

    print(metrics)
    print(f"Best model by AUROC: {best_name}")

if __name__ == "__main__":
    main()
