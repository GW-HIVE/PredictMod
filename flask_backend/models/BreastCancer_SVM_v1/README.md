# 🧬 Breast Cancer Treatment Response Prediction  
### Single-Cell RNA-seq–based Machine Learning Pipeline

---

## 📌 Project Overview

Triple-Negative Breast Cancer (TNBC) patients typically receive either **Chemotherapy** or **Anti–PD-L1 + Chemotherapy**. However, only a subset of patients respond effectively to each treatment.

This project builds **two machine learning models** using **pre-treatment single-cell RNA-seq data** to:

- Predict response likelihood for **Chemotherapy**
- Predict response likelihood for **Anti–PD-L1 + Chemotherapy**
- Aggregate **cell-level predictions** into a **patient-level response estimate**

The system is designed for **real-world inference**, where each patient may contribute **multiple single-cell observations**.

---

## 🎯 Objective

- Use **pre-treatment immune cell features** to predict treatment response
- Build **separate, treatment-specific models**
- Prevent **data leakage** by respecting patient-level grouping
- Provide a **deployable and interpretable inference pipeline**

---

## 📊 Data Source

**Primary Publication**  
*Single-cell analyses reveal key immune cell subsets associated with response to PD-L1 blockade in triple-negative breast cancer*  
**PMID:** 33589889  
**GEO Accession:** GSE169246

**Data Characteristics**
- Single-cell RNA sequencing (scRNA-seq)
- Pre-treatment immune cells
- Multiple cells per patient
- Cell-level annotations linked to patient response

---

## 🧪 Dataset Structure

Each row corresponds to **one immune cell**.

| Column | Description |
|------|-------------|
| Expression | Aggregate gene expression score |
| nUMI | Total RNA molecules per cell |
| nGene | Number of detected genes |
| percent_mito | Mitochondrial gene fraction (cell stress) |
| percent_hsp | Heat shock protein expression |
| percent_ig | Immunoglobulin expression |
| percent_rp | Ribosomal protein expression |
| PDCD1 | PD-1 gene expression |
| Origin | Tissue source |
| Response | Clinical response label |
| Patient_code | Unique patient identifier |
| Timeline | Pre-treatment / Post-treatment |

---

## 🧠 Modeling Strategy

### Why two models?

Different treatments were trained on **different tissue distributions**:

- **Chemo model**
  - `breast`, `liver`
- **Anti–PD-L1 + Chemo model**
  - `chest_wall`, `liver`, `lymph_node`

Training a single model would introduce **distribution shift**, so treatment-specific models are used.

---

## 🤖 Models Used

- **Support Vector Machine (SVM)**
  - RBF kernel
  - Class-weight balanced
  - StandardScaler included in pipeline

**Why SVM?**
- Suitable for small datasets
- Handles non-linear decision boundaries
- Stable under limited samples

---

## 🔍 Prediction Logic

1. User uploads a CSV containing **single-cell observations**
2. Data is filtered to **pre-treatment** rows
3. Tissue origin is **one-hot encoded**
4. Each model:
   - Receives only the features it was trained on
   - Produces **cell-level predictions**
5. Final response score:

    percentage = (Number of responder cells / Total number of cells) * 100

---

## Train the model

`python chemo_model_training.py --input "path/to/your/data.csv"`

`python combo_model_training.py --input "path/to/your/data.csv"`

## Run the model

`python test_script.py --input "path/to/your/testdata.csv" --model "chemo_model.pkl"`

`python test_script.py --input "path/to/your/testdata.csv" --model "combo_model.pkl"`