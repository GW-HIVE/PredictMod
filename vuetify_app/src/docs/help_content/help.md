
# Table of Contents  

<br>

## What is PredictMod?  
 The PredictMod platform utilizes machine learning tools and complex datasets based on electronic health records, gut microbiome, and -omics data to forecast patient outcomes, often in response to treatment for a particular condition.  
  
<br>
  
#### Additional Resources:
[About us](https://hivelab.biochemistry.gwu.edu/predictmod/about)  
[Frequently Asked Questions (FAQ)](https://hivelab.biochemistry.gwu.edu/predictmod/faq)  
[Contact us](https://hivelab.biochemistry.gwu.edu/predictmod/contact)  
  
<br>  
  
## Login & Registration
### <a id="how-to-register">How to register with PredictMod</a>  
Individuals interested in creating a PredictMod account should do so through the _Login_ page. If you have any questions, please contact us at mazumder_lab@gwu.edu. 
  
<br>  
  
### <a id="login-faqs">Login & registration FAQs</a>   

<br>  
  
#### Who can register for a PredictMod account?  
Any clinicians, and researchers, or other individuals interested in using the tool are invited to register.  
#### How long does registration last?  
Registered accounts do not expire. You will be logged out after 24 hours of each login.  
#### Will the system store patient data?  
The data will not be saved in the system. PredictMod will use uploaded patient data to make a one-time prediction.  
#### Can I view a history of my predictions?  
Prediction results are not saved, so a prediction history is not available.  
  
<br>  
  
## 'Try it Out' Example Query Builder
#### <a id="tio-query-builder">How the example query builder works</a>  
The example query builder is distinct from the standard query builder in that only the example prediction file is accepted. You cannot upload your own single-patient files into the example query builder and obtain a prediction.  

You can build an example query by selecting the condition, intervention, and data type of interest to you. Based on these selections, an example data file will be available for download.  

You should use example data files as a template for your own data upload.  
  
<br>  
  
#### <a id="example-downloads">Download example data</a>   
Example data files for each model are provided in the query builder.
  
<br>  
  
## <a id="current-models">Current Models</a>  
Current and anticipated models are shown on the _Models_ page.    
<br>  

## Query Builder
  
<br>  
  
### <a id="query-builder">How the query builder works</a>  
The query builder determines the appropriate model to use for a prediction, based on the desired condition, intervention, and data type. Please follow the prompts on the Query Builder page to make your selections. Descriptions of the conditions, interventions, and data types are documented within each Model's BioCompute Object (BCO). You will then be able to upload your own file or download an example file. The uploaded file must meet the formatting requirements associated with the chosen model. For information on formatting, please review the sample data, FAQs, or contact our team. 
  
<br>  

  
### <a id="file-formats">Formatting FAQs</a>  
  
<br>  
  
**What file types are accepted?**  
Comma separated values (csv) or excel workbook (xlsx) files are accepted.   
  
**How do I know if my file is not formatted correctly?**  
An incorrectly formatted file will return an error message when the 'Run a Prediction' option is selected.   
  
If you receive a formatting error message and you are unsure why, please contact our team and we can work with you to resolve the issue. 
  
<br>  
  
### <a id="run-sample">Run a prediction</a>  
Once a correctly-formatting file has been uploaded, select ‘Run Prediction’ to view your results.  
  
### <a id="interpreting-results">Interpreting a prediction result</a>    
  
#### <a id="r-nr">Responder vs. Non-Responder outcomes</a>  
PredictMod will provide a prediction categorized as either Responder or Non-Responder. The outcomes associated with the response status vary for each model, though a Responder result is generally associated with a positive health outcome, and the Non-Responder result is generally associated with a negative health outcome.  
  
#### <a id="visualization">Data visualization examples and interpretations</a>  
The primary data visualization tool is a SHAP force plot. Shapley Value originates from game theory and involves the fair distribution of reward based on the degree of contribution of each player. This can be utilized in precision medicine to identify the key “players” or features that contribute to a given prediction. The SHAP (SHapley Additive exPlanations) Force Plot leverages this ideology to provide Explainable AI with respect to the single patient predictions made by PredictMod. Each plot for a given prediction not only indicates the most influential features but highlights whether that feature pushes the prediction higher (in red) or lower (in blue). The consideration of the features and their values leads to a score, where higher scores indicate a prediction of 1, or NR and lower scores a prediction of 0, or R. SHAP Force Plots also indicate the degree of feature impact based on proximity to the boundary line where the red and blue bars meet. The closer to the dividing boundary, the more impact that feature had on the patient’s prediction.
  
<br>  
  
### <a id="new-prediction">Run another prediction</a>
Selecting 'Run Another Prediction' will return you to the query builder page, where you can complete steps 1 through 4 to run a new prediction. As a reminder, no patient data is stored in the PredictMod server, so running another prediction will erase any currently displayed results.  
    
<br>  
  
## <a id="publish">Upload a Model</a>
PredictMod is a collaborative space for researchers to upload their intervention-based models and performance metrics. These models are freely available to users and commercial entities under the CC BY 4.0 license. While our current focus is Prediabetes, the platform allows for multiple models to overlap among conditions and interventions. Researchers can upload their model and relevant documentation directly to PredictMod to make it freely available to users.
    
<br>  
  
