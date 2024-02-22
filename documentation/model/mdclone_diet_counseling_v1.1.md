# MDClone_Diet_Counseling_v1.1
The following information provided in this document details our process for data preprocessing, algorithm selection, hyperparameters, model evaluation, and quality control. Additionally, the goal of this document is to highlight source code associated with each iteration of the MDClone model.

**Data Source**  
MDClone (https://www.mdclone.com) is a synthetic patient data platform that has a collaboration with the Veterans Affairs to generate synthetic patients that exhibit similar statistics to US veterans. This allows for data transfer internally and externally without the compromise of any personal patient information. MDClone provides the ability to connect several health service entities to consolidate patient data into a single platform which provides less gaps in documented visits and care. 

The training dataset included 19,842 patients and 19 variables.

**Intervention & Outcomes** 
A responder status is based on a resulting weight at least 5% lower than their starting weight. The resulting weight is the lowest weight collected within a 6-month timeframe, following the start of the intervention. A nonresponder status is based on less than 5% weight loss, or any amount of weight gain as the lowest weight collected within the 6-month timeframe.

**Algorithm & Model Performance**  
A Decision Tree Classifier (DTC) was used, as it performed the best when compared to other algorithms, with 97% accuracy. 
