# README  
### Existing Models:    
**MG_Exercise_v1.1:**  
Metagenomic DTC model with 89% accuracy. Trained on open-source data with 40 patients and 281 genomes. v1.1 released on 05.31.2023.  
* Condition: Prediabetes
* Intervention: Exercise
* Data Type: Metagenomic

**MDClone_Diet_Counseling_v1.1:**   
EHR XGBoost model with 67% accuracy. Trained on synthetic veteran patient data from MDClone, with 19,842 patients and 19 variables. v1.1 released on 12.11.2023.  
* Condition: Prediabetes
* Intervention: Dietary Counseling
* Data Type: EHR
  
**PredictMod_EHR_Keto_v1.0:**   
EHR SVM model with 65% accuracy. Trained on US patient data from Epic Cosmos, with 308 patients and 26 variables. v1.0 released on 02.29.2024.  
* Condition: Prediabetes
* Intervention: Keto Diet
* Data Type: EHR

**Diabetes_glycomic_v1:**   
XGBoost model predicting whether patient will develop type 2 diabetes or remain normoglycaemic within 10 years, based on N-glycomic data.    
* Condition: Type 2 Diabetes Mellitus
* Intervention: Null (No Intervention)
* Data Type: Glycomic

**ccRCC_glycoproteomic_v1:**   
Logistic regression model predicting whether the patient is at high or low risk of death or disease progression within 5 years from tumor resection, based on N-glycoproteomic data.
* Condition: Clear cell renal cell carcinoma
* Intervention: Null (No Intervention)
* Data Type: Glycoproteomic

### Anticipated Models: 
**Epilepsy_Keto_v1.1:**   
MG Logistic Regression model predicting 50% reduction in seizure frequency following a ketogenic diet intervention.  
* Condition: Epilepsy
* Intervention: Keto Diet
* Data Type: Metagenomic

**Synthea_Exercise_v1.1:**   
EHR model predicting diagnosis of Type 2 Diabetes Mellitus following a lifestyle change intervention. Based on synthetic patient data.  
* Condition: Prediabetes
* Intervention: Exercise
* Data Type: EHR

**MDClone_Diet_Counseling_v1.2:**   
Improved MDClone_Diet_Counseling_v1.1 model, based on synthetic veteran patient data from MDClone.  
* Condition: Prediabetes
* Intervention: Dietary Counseling
* Data Type: EHR

**MDClone_Semaglutide_v1.0:**   
EHR model predicting 5% reduction in weight following a semaglutide intervention. Based on synthetic veteran patient data from MDClone.  
* Condition: Prediabetes
* Intervention: Semaglutide
* Data Type: EHR

**MDClone_Exercise_v1.0:**   
EHR model predicting 5% reduction in weight following an exercise intervention. Based on synthetic veteran patient data from MDClone.  
* Condition: Prediabetes
* Intervention: Exercise
* Data Type: EHR


