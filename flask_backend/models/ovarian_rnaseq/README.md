# **Data Preprocessing, Algorithm Selection, and Model Evaluation for RNA-Seq Classifier**

## **Data Source**  
RNA-Seq data was derived from ovarian cancer patients undergoing treatment. This dataset is used to develop a classifier for predicting patient responsiveness to treatment, specifically their likelihood to exhibit tumor size reduction.  

---

## **Training Dataset**  
The dataset consists of patient RNA-Seq profiles, with expression values reported as TPM (Transcripts Per Million). TPM was chosen over FPKM because TPM ensures consistency across samples by normalizing for total read counts, making it better suited for cross-sample comparisons. Attempts to curated data included Spearman Correlation, Volcano plots, and PCA. Current feature selection based on the top features exhibiting the highest range dispersion.

Gene expression used for final Model have appeared to pick up genes that could potentially be of additional research (FASTA file with genes within the fasta zipped file)

---

## **Classifier and Predictor**  
### **Classifier Code:**  
#### **Preprocessing:**  
- **Load Data:**  
  The RNA-Seq data is read from a collection of `.txt.gz` files, which are concatenated into a single dataset for analysis. Each file contains columns for `gene_id` and `TPM`.  
- **Train-Test Split:**  
  The data is split into training and testing sets using `train_test_split` with an 80/20 ratio.  
- **Class Balancing:**  
  The Synthetic Minority Oversampling Technique (SMOTE) is applied to address class imbalance in treatment response labels.  

#### **Model Training:**  
- **Classifier Selection:**  
  A Random Forest classifier is chosen for its robustness to high-dimensional data.  
- **Training:**  
  The model is trained on the preprocessed RNA-Seq data.  
- **Serialization:**  
  The trained classifier, feature names, and preprocessing pipeline are saved as `.pkl` files using `joblib`.  

#### **Model Evaluation:**  
- **Prediction:**  
  Predictions are made on the test set using the trained classifier.  
- **Performance Metrics:**  
  - Accuracy: Evaluates overall model correctness.  
  - ROC-AUC: Assesses the ability of the model to distinguish between responder and non-responder classes.  
  - Classification Report: Provides precision, recall, and F1 scores for each class.  

---

### **Predictor Code:**  
#### **Preprocessing:**  
- **Load Model:**  
  The pre-trained classifier and preprocessing pipeline are loaded from `.pkl` files.  
- **Load New Data:**  
  New RNA-Seq data from a single patient is loaded and preprocessed to match the training pipeline.  

#### **Prediction:**  
- **Make Prediction:**  
  The classifier predicts treatment responsiveness for the new patient.  
- **Output Result:**  
  The predicted class is decoded and displayed for clinical interpretation.  

---

## **Intervention & Outcomes**  
- **Responder Status:**  
  Patients who are predicted to respond positively to treatment, with a significant reduction in tumor size.  
- **Non-Responder Status:**  
  Patients who are predicted to show minimal or no reduction in tumor size.  

---

## **Algorithm & Model Performance**  
- **Algorithm:**  
  Random Forest Classifier  
- **Model Accuracy:**  
  75%  
- **ROC-AUC:**  
  0.81 

---

## **Key Insights**  
- Using TPM normalization ensures robust cross-sample comparisons, improving model reliability.  
- SMOTE effectively addresses class imbalance, enabling more accurate predictions for underrepresented classes.  
- This model supports personalized treatment decisions by identifying potential responders and non-responders based on RNA-Seq profiles.
- Raw Data used for model training available at https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE188249

