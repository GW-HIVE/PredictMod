# PredictMod Submission Checklist

## Included

- [x] ML-ready training dataset
- [x] Clear binary outcome column: Tumor Free vs With Tumor
- [x] Training script
- [x] Multiple model algorithms
- [x] Accuracy, AUROC, F1, precision, and recall
- [x] Confusion matrices
- [x] Feature-selection results
- [x] SHAP summary plot
- [x] Saved best-model bundle
- [x] Single-patient prediction script
- [x] README and model card
- [x] BioCompute Object JSON
- [x] Human-readable BCO Markdown

## Files to verify before opening the pull request

- [ ] `data/tcga_lihc_tumor_status_ml_ready_top500_genes.csv.gz`
- [ ] `scripts/train_models.py`
- [ ] `scripts/single_patient_predict.py`
- [ ] `models/best_model_bundle.joblib`
- [ ] `results/model_metrics_comparison.csv`
- [ ] `figures/best_model_confusion_matrix.png`
- [ ] `figures/shap_summary_plot.png`
- [ ] `docs/tcga_lihc_tumor_status_bco.json`

## Reviewer notes

- The outcome is follow-up tumor status, not a controlled treatment-response endpoint.
- Random Forest was the strongest held-out baseline by AUROC.
- The current SHAP plot explains XGBoost, not Random Forest.
- Prior-treatment variables require a temporal leakage audit.
- This model is for exploratory research and training only, not clinical use.
