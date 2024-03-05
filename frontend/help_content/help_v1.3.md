
# Table of Contents  
## What is PredictMod?  
 The PredictMod platform utilizes machine learning tools and complex datasets based on electronic health records, gut microbiome, and -omics data to forecast patient outcomes, often in response to treatment for a particular condition.

#### Additional Resources:
About us > [https://hivelab.biochemistry.gwu.edu/predictmod/about]  
Frequently Asked Questions (FAQ) > [https://hivelab.biochemistry.gwu.edu/predictmod/faq]  
Contact us > [https://hivelab.biochemistry.gwu.edu/predictmod/contact]  

## Login & Registration
### How to register with PredictMod  
Individuals interested in creating a PredictMod account should contact mazumder_lab@gwu.edu. Our team will follow up with you to provide login credentials. An automatic registration tool is coming soon.

### Login & registration FAQs 
#### Who can register for a PredictMod account?  
Students, clinicians, and researchers interested in using the tool are invited to register. 
#### How long does registration last?  
Registered accounts do not expire. You will be logged out after 24 hours of each login. 
#### Will the system store patient data?  
The data will not be saved in the system. PredictMod will use uploaded patient data to make a one-time prediction. 
#### Can I view a history of my predictions?  
Prediction results are not saved, so a prediction history is not available.

## 'Try it Out' Example Query Builder
#### How the example query builder works  
The example query builder is distinct from the standard query builder in that only the example prediction file is accepted. You cannot upload your own single-patient files into the example query builder and obtain a prediction. 

You can build an example query by selecting the condition, intervention, and data type of interest to you. Based on these selections, an example data file will be available for download. 

You should use example data files as a template for your own data upload.

#### Download example data   
Example data files for each model can be found below: 

MG_Exercise_v1.1: _mg_exercise_v1.1_example.csv_
MDClone_Diet_Counseling_v1.1: _mdclone_diet_counseling_v1.1_example.csv_
PredictMod_EHR_Keto_v1.1: _predictmod_ehr_keto_v1.0_example.csv_

## Current Models
#### MG_Exercise_v1.1 
Readme.md file at [https://github.com/GW-HIVE/PredictMod/tree/main/models]
#### MDClone_Diet_Counseling_v1.1
Readme.md file at [https://github.com/GW-HIVE/PredictMod/tree/main/models]
#### PredictMod_EHR_Keto_v1.0
Readme.md file at [https://github.com/GW-HIVE/PredictMod/tree/main/models]

## Anticipated Models
#### Glycomics_PreDM_v1.0
Glycomics model predicting diagnosis of Type 2 Diabetes Mellitus.

#### Epilepsy_Keto_v1.1  
MG Logistic Regression model predicting 50% reduction in seizure frequency following a ketogenic diet intervention.

#### Synthea_Exercise_v1.1  
EHR model predicting diagnosis of Type 2 Diabetes Mellitus following a lifestyle change intervention. Based on synthetic patient data.

#### MDClone_Diet_Counseling_v1.2  
Improved MDClone_Diet_Counseling_v1.1 model, based on synthetic veteran patient data from MDClone.

#### MDClone_Semaglutide_v1.0  
EHR model predicting 5% reduction in weight following a semaglutide intervention. Based on synthetic veteran patient data from MDClone.

#### MDClone_Exercise_v1.0  
EHR model predicting 5% reduction in weight following an exercise intervention. Based on synthetic veteran patient data from MDClone.

## Query Builder
### How the query builder works  
The query builder determines the appropriate model to use for a prediction, based on the desired condition, intervention, and data type. 

The uploaded file must meet the formatting requirements associated with the chosen model. For information on formatting, please review the sample data, FAQs, or contact our team. 

### Step 1: selecting a condition  
Currently, the condition of interest is Prediabetes. We have an epilepsy model coming soon. 

**About the _Prediabetes_ condition:** 
Prediabetes is a precursor to Type 2 Diabetes Mellitus (T2DM), where blood sugars are higher than normal, but not high enough to be considered T2DM. Prediction outcomes are based on a 5% reduction in weight, HOMA-IR, or a diagnosis of T2DM.

### Step 2: selecting an intervention
The current interventions are exercise, ketogenic diet, and dietary counseling. We also have a Semaglutide intervention coming soon.

**About the _Exercise_ intervention:**  
An exercise intervention involves adherence to an exercise regimen recommended by a clinician or researcher. This is a common recommendation for individuals with prediabetes.

**About the _Diet - Keto Diet_ intervention:**  
A ketogenic diet, commonly known as a 'keto diet', involves a strict reduction in carbohydrate intake. This intervention has been associated with improved outcomes in individuals with prediabetes and epilepsy.

**About the _Diet - Dietary Counseling_ intervention:**  
Dietary counseling refers to receiving a clinician recommendation to improve dietary intake. These recommendations are typically tailored to the condition of interest. For example, a low carbohydrate diet is typically recommended for individuals with prediabetes.

### Step 3: selecting a data type
The current data types are metagenomic (MG) and electronic health record (EHR). We also have a glycomics data type coming soon.

**About the _Gut Microbiome_ data type:**
Metagenomic (MG) data consist of the microbial composition of the gut microbiome typically displayed as a percent of abundance. This data is typically used within a research context to profile healthy gut microbiomes and to identify differential abundances and their associations to disease. Our MG Model is trained on publicly available data. The reference genomes used for this model are recorded in the Gut Feeling Knowledge Base (GFKB). Please use this list as a reference. Organisms not referenced in the GFKB can still be included in the input and receive an accurate model prediction. If you have any questions about this, please don’t hesitate to contact our team. 

**About the _Electronic Health Records_ data type:**
Electronic Health Records (EHR) consists of real-time patient-centered records that are utilized by physicians to streamline their workflow. It provides physicians the ability to view important medical details about their patients in order to provide improved patient care that is both efficient and safe. Our EHR models are trained on data from the MDClone and Epic Cosmos.

### Step 4: uploading a data file
Once you make your selection, upload a file (either one of our example files, or one of your own single-patient data files). 

The uploaded file must meet the formatting requirements associated with the chosen model. For information on formatting, please review the sample data, FAQs, or contact our team. 

#### Formatting FAQs
**What file types are accepted?**  
Comma separated values (csv) or excel workbook (xlsx) files are accepted. 

**How do I know if my file is not formatted correctly?**  
An incorrectly formatted file will return an error message when the 'Run a Prediction' option is selected. 

If you receive a formatting error message and you are unsure why, please contact our team and we can work with you to resolve the issue. 

### Run a prediction  
Once a correctly-formatting file has been uploaded, select ‘Run Prediction’ to view your results.

### Interpreting a prediction result
#### Responder vs. Non-Responder outcomes
 PredictMod will provide a prediction categorized as either Responder or Non-Responder. The outcomes associated with the response status vary for each model, though a Responder result is generally associated with a positive health outcome, and the Non-Responder result is generally associated with a negative health outcome.

#### Data visualization examples and interpretations
The primary data visualization tools are a decision tree and a SHAP force plot.

Shapley Value originates from game theory and involves the fair distribution of reward based on the degree of contribution of each player. This can be utilized in precision medicine to identify the key “players” or features that contribute to a given prediction. The SHAP (SHapley Additive exPlanations) Force Plot leverages this ideology to provide Explainable AI with respect to the single patient predictions made by PredictMod. Each plot for a given prediction not only indicates the most influential features but highlights whether that feature pushes the prediction higher (in red) or lower (in blue). The consideration of the features and their values leads to a score, where higher scores indicate a prediction of 1, or NR and lower scores a prediction of 0, or R. SHAP Froce Plots also indicate the degree of feature impact based on proximity to the boundary line where the red and blue bars meet. The closer to the dividing boundary, the more impact that feature had on the patient’s prediction.

### Run another prediction
Selecting 'Run Another Prediction' will return you to the query builder page, where you can complete steps 1 through 4 to run a new prediction. As a reminder, no patient data is stored in the PredictMod server, so running another prediction will erase any currently displayed results.

## Coming Soon: Upload a Model
Uploading your machine-learning model
Model review & verification process
Model upload FAQs
