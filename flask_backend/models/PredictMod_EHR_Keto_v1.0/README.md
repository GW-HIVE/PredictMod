# PredictMod_EHR_Keto_v1.0 
**Data Source**  
Epic Cosmos (https://www.cosmos.epic.com) is a health record database that compiles clinical data points from several EMR systems to consolidate patient information. The aim of Cosmos is to provide this information to advance health care research. Currently, Cosmos contains 196 million recorded patients with 7.8 billion encounters documented. Additionally, Cosmos is the largest integrated database for clinical information in the United States that contains patients representing the general statistics of the US population. Cosmos contains longitudinal data spanning several years of visits per patient. The charts are also integrated to contain both in-patient and out-patient charts to provide a clear and connected view of each patient’s medical history. 

The training dataset included 308 patients and 26 variables.

**Intervention & Outcomes** 
The intervention of interest for this model is the ketogenic diet. A responder status is based on a resulting weight at least 5% lower than their starting weight. The resulting weight is the lowest weight collected within a 6-month timeframe, following the start of the intervention. A nonresponder status is based on less than 5% weight loss, or any amount of weight gain as the lowest weight collected within the 6-month timeframe.

**Algorithm & Model Performance**  
Support Vector Machine (SVM) is a type of supervised ML that aims to classify objects into two or more categories. The SVM with sigmoid kernel performed the best (65% accuracy) compared to all other kernels. This is likely due to the sigmoid kernel being used for binary classification problems where the data points are not linearly separable in the input space.

Link to Tutorial: https://colab.research.google.com/drive/1dkZRwe_4EPduPkYBVWYOfjt6JBaQhjwu#scrollTo=it3WkUydjEmv
