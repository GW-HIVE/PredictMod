## FAQ
**How can I run a prediction using a single-patient data file?**  
Use the query builder to select the desired condition, intervention, and data type associated with your patient data. File upload templates vary by model. Reference our example files to ensure your data meets our formatting requirements. Select ‘Run Prediction’ to view the results. 

For additional assistance with uploading and formatting data, please contact our team.

**Will the system store patient data?**  
The data will not be saved in the system. PredictMod will use uploaded patient data to make a one-time prediction.

**What are the possible prediction outcomes?**
PredictMod will provide a prediction categorized as either _Responder_ or _Non-Responder_. The outcomes associated with the response status vary for each model, though a _Responder_ result is generally associated with a positive health outcome, and the _Non-Responder_ result is generally associated with a negative health outcome. 

For additional information, please review the model information below. 

**What data types are includd in the PredictMod query selection?**  
The current data types are metagenomic (MG) and electronic health record (EHR). We also have a glycomics data type coming soon.

_MG data_ consist of the microbial composition of the gut microbiome typically displayed as a percent of abundance. This data is typically used within a research context to profile healthy gut microbiomes and to identify differential abundances and their associations to disease. Our MG Model is trained on publicly available data. The reference genomes used for this model are recorded in the Gut Feeling Knowledge Base (GFKB). Please use this list as a reference. Organisms not referenced in the GFKB can still be included in the input and receive an accurate model prediction. If you have any questions about this, please don’t hesitate to contact our team. 

_EHR_ consists of real-time patient-centered records that are utilized by physicians to streamline their workflow. It provides physicians the ability to view important medical details about their patients in order to provide improved patient care that is both efficient and safe. Our EHR models are trained on data from the MDClone and Epic Cosmos.

**What conditions are included in the PredictMod query selection?**  
The current condition of interest is Prediabetes. We also have an Epilepsy model coming soon.

_Prediabetes_ is a precursor to Type 2 Diabetes Mellitus (T2DM), where blood sugars are higher than normal, but not high enough to be considered T2DM. Prediction outcomes are based on a 5% reduction in weight, HOMA-IR, or a diagnosis of T2DM.

**What interventions are included in the PredictMod query selection?**  
The current interventions are exercise, ketogenic diet, and dietary counseling. We also have a Semaglutide intervention coming soon.
