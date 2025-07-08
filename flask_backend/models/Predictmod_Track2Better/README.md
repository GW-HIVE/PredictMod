# CGM_TrueHealthy_Study_v1.0

## Data Source
This project uses the AI-READI dataset focused on continuous glucose monitoring (CGM) data collected using Dexcom G6 sensors. Each participant has time-series blood glucose data recorded every 5 minutes, across ~7 days (~2138 records). The dataset originally included 1049 participants, with 784 selected for clean and consistent glucose records.

## Intervention & Outcomes
We observed that the "healthy" group included misclassified individuals. By using unsupervised learning (K-Means clustering), we identified a subset of participants whose glucose patterns aligned with clinical expectations for truly healthy individuals. These were labeled as "true_healthy". We then trained supervised models to identify similar patterns in other study groups and relabeled iteratively.

## Algorithm & Model Performance
A K-Means clustering approach was applied to engineered features (mean glucose, std dev, CV%, TIR%, TAR%, TBR%, etc.) to extract true_healthy participants. An XGBoost classifier trained on these refined labels was able to detect misclassified healthy individuals from other groups. Later, an LSTM model was built using time-series features and SMOTE for balancing, achieving high recall and AUC (>0.79) in distinguishing true_healthy from prediabetes.

## CGM Python Predict - Workflow
The workflow includes:
- Cleaning and batch processing glucose data.
- Engineering time-based and statistical features.
- Label refinement using K-Means clustering.
- Classification using XGBoost.
- Time-series classification using LSTM.
