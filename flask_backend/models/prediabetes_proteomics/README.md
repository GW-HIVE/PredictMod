# prediabetes_proteomics_model
The following information provided in this document details our process for data preprocessing, algorithm selection, hyperparameters, model evaluation, and quality control. Additionally, the goal of this document is to highlight source code associated with each iteration of the MDClone model.

## Data Source 
This dataset was retrieved from a publication interested in identifying the protein-related predictors for exercise. 
The training dataset included 48 patients and 688 variables.

## Intervention & Outcomes 
The intervention consisted of a 12-week high-intensity interval exercise training program for medication-naïve overweight or obese men with prediabetes.

## Algorithm & Model Performance 
A Random Forest Classifier was employed, with data preprocessing incorporating the Synthetic Minority Oversampling Technique (SMOTE) and Leave-One-Out Cross-Validation (LOOCV) to address class imbalance and the relatively small dataset size.

## Algorithm Stats
**Overall Accuracy:** 0.8971

**Overall F1 Score:** 0.8971


