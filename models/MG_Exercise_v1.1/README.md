# MG_Exercise_v1.1  
**Data Source**  
Our MG_Exercise Model is trained on metagenomic whole-genome sequencing (WGS) reads stored within the National Center for Biotechnology Information’s (NCBI) Sequence Read Archive (SRA). These reads were submitted by authors of a publication (PMID 31786155) interested in identifying alterations within gut microbiome profiles of medication-naïve prediabetes male volunteers. 

The training dataset included 40 patients and 281 variables.

**Intervention & Outcomes** 
The volunteers of this study were separated into a sedentary and an exercise group, where the exercise group underwent a 12-week high-intensity exercise regimen. The authors observed a varied response to the intervention within their experimental group, with some individuals experiencing a favorable outcome (a 2-fold or greater reduction in Homeostatic Model Assessment for Insulin Resistance (HOMA-IR)), while others showed little to no improvement in HOMA-IR. Those who were able to improve their HOMA-IR were deemed responders in this study, while those who were unable to improve their condition were deemed non-responders. 

**Algorithm & Model Performance**  
A decision tree classifier (DTC) was chosen as the algorithm to be trained with metagenomic data given the dataset consisted of 200+ features. DTCs are particularly good at determining which features are most helpful to make accurate predictions and are likely to forgo features that may not aid in prediction accuracy. This is opposed to an algorithm such as linear regression, that may require use of all provided features to make predictions. This can often lead to a lower accuracy and model confusion; therefore, a DTC was implemented for generating predictions off of metagenomic data. The DTC was able to perform at 90% accuracy with a 0.9 area under the curve (AUC) with a dataset containing 20 responders and 20 non-responders.

### MG Python Predict - Workflow
The python prediction module has been separated to allow creation & training of the decision tree, followed by "pickling" (ie, storing long term or "preserving" the tree). The pickle is then read & restored to a python object in a separate script, which uses the tree to perform prediction. The workflow is as follows:
1. Create a tree: `python create_tree.py`
2. Use the tree to perform a prediction: `python use_tree.py`

Use/updates by the PredictMod interface requires manually copying the pickled object to the `matlab-interface` directory. 

# NB
In general, binary objects (including Excel files, pdfs, etc.) should not be stored in GitHub. In line with that, the pickle must be created locally using `create_tree.py`. The `.gitignore` file has been updated to ignore `*.pickle` files, generally.
