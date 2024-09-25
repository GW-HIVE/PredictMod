# Tutorial: Integration of a Machine Learning-based Approach for Predictive Clinical Decision-making using Python
ADD IMAGE
## Summary
### Part I. Machine Learning Using Python
1. What is Python?
2. Objectives
3. Methodology of the Machine Learning Algorithms
4. Software Installation
5. Downloading the Input Files for Synthetic Data Generation
6. Downloading the Input Files for Model Training
   
### Part II. Using Python scripts to detect signal difference in the Electronic Healthcare Records of responsive and unresponsive patients	8
1. Process
2. Interpreting the Results
3. Further Analysis and Next Steps
   
## Part I. Machine Learning Using Python
### 1. What is Python?
Python is a versatile programming language that supports multiple programming paradigms, including procedural, object-oriented, and functional programming. It is widely used for tasks such as data manipulation, web development, scientific computing, and automation. Python’s extensive standard library and external packages make it particularly useful for data analysis, machine learning, and visualization. Through libraries like NumPy, pandas, matplotlib, and scikit-learn, Python excels at handling large datasets, building models, and visualizing results. Additionally, Python can easily interface with programs written in other languages and supports the integration of a wide range of toolkits to extend its functionality.

### 2. Objectives
The general purpose of this protocol is to provide proof-of-concept through a Python workflow for creating predictive machine learning models using some form of data. In this tutorial, patient data will serve as an example input into the system while the output will determine whether the patient is a responder or a non-responder to the treatment assigned. The concepts in this tutorial will be applicable to most binary classification datasets for future model development. 

Two major machine learning concepts will be applied to this system as follows:  
1. Create a synthetic data set to be used as an input to a machine learning model to ensure consistency during the model training steps 
2. Input patient data through a series of machine learning classification models to predict whether or not a treatment is effective before dietary or medical intervention (e.g. responder vs. non-responder)

This tutorial utilizes patient data provided by [Synthea](https://synthea.mitre.org/downloads). The process of how Synthea data was retrieved and filtered using MATLAB can be found in this [link](https://docs.google.com/document/d/1yfUjoaU0lfTx8blTCgZehR7Qdn0C0iTU3VTPAag9ITI/edit?usp=sharing). This tutorial has its own retrieve and filter process written in python that we will use. If interested the full synthetic generation process can be found at this [link](https://github.com/GW-HIVE/PredictMod/tree/main/flask_backend/models/Diabetes_EHR_v1)

### 3. Methodology of the Machine Learning Algorithms
1. Generating Synthetic Data: In order to generate synthetic data, the covariance, standard deviation, and mean are calculated for each variable (BMI, glucose etc.) from the patient dataset. The algorithm will also designate whether the variable is continuous or discrete. A “noise” data set is then generated based on these statistical calculations. This “noise” data is then refined when two classifier neural networks compete to label the data appropriately based on the training set. Once the synthetic data is labeled appropriately, it is stored in a matrix and this process is repeated until a sufficient number of values are generated. This algorithm is similar to a Generational Adversarial Network (GAN). More information regarding how GANs work can be found through the following [link](https://en.wikipedia.org/wiki/Generative_adversarial_network). The purpose of the synthetic data generation step in this tutorial is to ensure that the multiple models we will apply to the dataset can handle the input data. Some traditional machine learning models cannot handle NAN/NULL values due to the mathematical operations involved in the process. Languages such as MATLAB that have built-in toolkits that account for this can take years to develop. Python does not have a library capable of this, so to avoid this issue, we can generate synthetic data that avoids this issue.

2. Classifying Training Data: A classification system utilizes a neural network or decision tree to create a binary classifier that can predict whether or not a patient (Row of data from the dataset) will be responsive (Label) to the standard Type II diabetes intervention plan. This plan involves non-invasive lifestyle changes such as diet and exercise. There are two identifiable classes for pre-diabetic individuals who follow the intervention plan: responders and non-responders. Responders are individuals who remain at prediabetic levels or return to normal levels while non-responders are individuals who develop diabetic levels after following the intervention plan. The machine learning algorithm is provided with a fraction of the original patient dataset, known as the “training set”, and trains the model to then be able to predict new patient data (“test set”) without knowing its label. 

### 4. Software Installation
Software Installation Requirements for running Machine Learning Algorithms
This guide provides step-by-step instructions on how to set up your environment for running the machine learning algorithm. Follow the instructions below to ensure that the necessary libraries and software are installed correctly.

*NOTE: There may be new versions of the software and libraries from when this tutorial was written. If you run into any issues with functions or methods being unusable, troubleshoot on forums such as stackoverflow or use older versions of software*

1. Install Python
First, ensure that Python is installed on your system. This tutorial uses Python 3.11. You can download Python from the official [website](https://www.python.org/downloads/)

2. Install VScode from the official [website](https://code.visualstudio.com/download) Ensure you are using the correct version based on your Operating System (O.S).
3. Configure VSCode to be able to run python following the instructions available on the official website: https://code.visualstudio.com/docs/python/python-tutorial. It is highly recommended to include Pylance: an extension that works alongside Python in Visual Studio Code to provide performant language support. Pylance can be added by opening visual studio code, clicking on the extensions on the left hand side and search for Pylance, and installing it.
4. Pip Install Python libraries required for this tutorial. PIP is the package installer for Python for libraries not included in the default python package. Run the following commands.
   `pip install tensorflow imageio matplotlib numpy pandas scikit-learn`
   *If for any reason Pylance cannot resolve an import of one of the required libraries, check which libraries you have installed by typing pip list in Visual Studio Code*

### 5. Downloading the Input Files for Synthetic Data Generation
Download the required material for this tutorial from this [link](https://drive.google.com/drive/folders/1U-TIZe-Iqmziijiiw-1VHZNaGhIXUerQ?usp=drive_link). The Synthetic Generation folder contains the python file and input excel files required for generating the dataset that we will use
**Python Project Materials List:**
Python Script Files:
**Synthetic_EHR_data_diabetes.py:** A Python script that generates synthetic Electronic Health Record (EHR) data for diabetes-related studies, using GAN techniques
Excel Data Files:
**label_non_responsive.xlsx:** Contains labels for non_responsive patient data
**label_responsive.xlsx:** Contains labels for responsive patient data
**data_non_responsive.xlsx:** Contains observational data related to patients non responsive to the treatment
**data_responsive.xlsx:** Contains observational data related to patients non responsive to the treatment
**var_list_.xlsx:** A list of variables or features that are present in the dataset. This can be used to identify key variables of interest during analysis.
Documentation:
**README.md**: A markdown file providing an overview of the project, explaining the purpose of the scripts, and instructions on how to use the code and data.
*The README contains information on a separate filter_format file that was used to curate the original synthea data into a digestible format for GAN techniques. Because this tutorial aims to demonstrate a machine learning model building workflow process, the format process for other datasets will differ. If you are interested in learning more, that process is available here: [MATLAB GAN](https://docs.google.com/document/d/1yfUjoaU0lfTx8blTCgZehR7Qdn0C0iTU3VTPAag9ITI/edit#heading=h.rqajp99xfplp)*

### 6. Downloading the Input Files for Model Training
Download the required material for this tutorial from this link. The model training folder contains the python file and input excel files required for testing multiple models and providing performance metrics.

Python Project Materials List:

Python Script Files:
multiple_model_analysis.py: A Python script that tests multiple traditional machine learning models on the input Electronic Health Record (EHR) data for diabetes-related studies
Excel Data Files:
EHR_data_1000patients.xlsx: Contains labels of patient data in first column, remaining columns are patient features (i.e blood pressure, sodium)


