# Tutorial: Integration of a Machine Learning-based Approach for Predictive Clinical Decision-making using Python
![alt text](images/image_tutorial.png)
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
- Python Project Materials List:
**Synthetic_EHR_data_diabetes.py:** A Python script that generates synthetic Electronic Health Record (EHR) data for diabetes-related studies, using GAN techniques
Excel Data Files:
**label_non_responsive.xlsx:** Contains labels for non_responsive patient data
**label_responsive.xlsx:** Contains labels for responsive patient data
**data_non_responsive.xlsx:** Contains observational data related to patients non responsive to the treatment
**data_responsive.xlsx:** Contains observational data related to patients non responsive to the treatment
**var_list_.xlsx:** A list of variables or features that are present in the dataset. This can be used to identify key variables of interest during analysis.
- Documentation:   
**README.md**: A markdown file providing an overview of the project, explaining the purpose of the scripts, and instructions on how to use the code and data.
*The README contains information on a separate filter_format file that was used to curate the original synthea data into a digestible format for GAN techniques. Because this tutorial aims to demonstrate a machine learning model building workflow process, the format process for other datasets will differ. If you are interested in learning more, that process is available here: [MATLAB GAN](https://docs.google.com/document/d/1yfUjoaU0lfTx8blTCgZehR7Qdn0C0iTU3VTPAag9ITI/edit#heading=h.rqajp99xfplp)*

### 6. Downloading the Input Files for Model Training
Download the required material for this tutorial from this link. The model training folder contains the python file and input excel files required for testing multiple models and providing performance metrics.

- Python Project Materials List:
Python Script Files:
**multiple_model_analysis.py:** A Python script that tests multiple traditional machine learning models on the input Electronic Health Record (EHR) data for diabetes-related studies
Excel Data Files:
**EHR_data_1000patients.xlsx:** Contains labels of patient data in first column, remaining columns are patient features (i.e blood pressure, sodium)

## Part II. Using Python scripts to detect signal difference in the Electronic Healthcare Records of responsive and unresponsive patients
**Process**
1.Create GAN model that will take input data and generate synthetic data within the same distribution of the initial data but without NAN/NULL values to avoid errors in later steps
2. Run multi-model analysis python script that tests a wide variety of machine learning models and outputs the accuracy and RMSE (Root Mean Squared Error) for each.
### Step 1 Creating Synthetic Data
1. Open VScode and in the top left corner, click on File -> Open Folder
2. Navigate to the folder where you have downloaded the Synthetic_EHR_data_diabetes.py
3. Once it has opened you should see the file explorer
4. Double click on the python file and it should show the script in the center of the page. On the top right of VScode, click the run python button
5. Make sure you are generating synthetic data for both the responsive dataset and non responsive dataset by adjusting what files the script is reading. Do so by adjusting data_responsive.xlsx to data_non_responsive.xlsx. Do the same for label_responsive.xlsx to label_non_responsive.xlsx. Make sure you do the same for the output xlsx file found at line 167:
`df.to_excel('EHR_responsive_at_epoch_{:04d}.xlsx'.format(epoch))`
`df.to_excel('EHR_non_responsive_at_epoch_{:04d}.xlsx'.format(epoch))`
6. You will need to concatenate the two synthetic files you generate from this process until it looks like this:
7. Make sure that the response column is filled out appropriately (0 for the non-responsive dataset and 1 for the responsive dataset)
### Step 2: Running the multi-model analysis
The multimodal analysis python script can be broken down into the following steps:
1. Load the dataset and extract X (features) and y (labels).
2. Split the data into training and testing sets.
3. Define a list of machine learning models to test.
4. Train each model and evaluate its performance (accuracy and RMSE).
5. Print results for each model.
All you need to do is run the python script and it will print the performance metrics in the terminal of VScode. This will provide you with a base to then determine which model will be the most effective in pursuing your more in-depth analysis as well as parameter and hyperparameter tuning. Please remember that curation of the data is an important step in the process of machine learning and ensure you have done what you could.

**Interpreting the Results**
Based on the results, we can observe that most models performed well on the dataset, with several models achieving high accuracy scores and low RMSE values. Below is a summary of the key findings and further suggestions for analysis.

**1. Logistic Regression:**
**Interpretation:** Logistic Regression performed decently with an accuracy of ~89.5%. However, the RMSE indicates that there's room for improvement in terms of prediction error. The confusion matrix shows some misclassification errors with 21 incorrect predictions in total (11 false positives and 10 false negatives).
**Next Steps:** Logistic Regression may benefit from **feature scaling** (standardization or normalization), **regularization** (such as L1 or L2 penalties), and **hyperparameter tuning** (for the regularization strength).

**2. Decision Tree**
**Interpretation:** The Decision Tree model achieved excellent accuracy (99%) with a very low RMSE, indicating strong predictive performance. The confusion matrix shows only two false negatives and no false positives.
**Next Steps:** While the Decision Tree performed very well, further improvements could involve pruning to avoid **overfitting**. **Hyperparameter tuning** (e.g., depth, minimum samples per split) and **ensemble techniques** (like boosting or bagging) could be explored to generalize the model further.

**3. Random Forest**
**Interpretation:** Random Forests also performed strongly, with an accuracy of 98% and a low RMSE. The model misclassified four samples, showing slightly less precision compared to Gradient Boosting but still very effective.
**Next Steps:** **Hyperparameter tuning** (number of trees, maximum depth, and minimum samples split) could further enhance Random Forest's performance. **Feature importance analysis** could also help to determine which features have the most impact on the model's predictions, allowing for potential data curation.

**4. Gradient Boosting:**
**Interpretation:** Gradient Boosting performed exceptionally well, achieving the highest accuracy (99.5%) and the lowest RMSE among the models tested. This suggests it handled both the class separability and prediction errors very effectively, with only one false negative and no false positives.
**Next Steps:** Tuning the **learning rate, number of boosting stages**, and **maximum depth** could further optimize this model. Additionally, feature selection or **dimensionality reduction** techniques like PCA (Principal Component Analysis) could be applied to reduce complexity and improve generalization.

**5. K-Nearest Neighbors (KNN):**
**Interpretation:** KNN achieved a reasonable accuracy of 94.5%, but the RMSE of 0.2345 suggests that its prediction error was slightly higher compared to tree-based methods. The confusion matrix shows that KNN had 11 false negatives, which could indicate issues with its distance-based approach on this dataset.
**Next Steps:** Scaling the data is crucial for KNN since it relies on distance measures. Additionally, **tuning the number of neighbors** (k) and trying different distance metrics (e.g., Euclidean, Manhattan) could improve performance. Dimensionality reduction like **PCA** might also help by removing noise and reducing computation time.

**6. Support Vector Machine (SVM):**
**Interpretation:** SVM had the lowest accuracy (81.5%) and highest RMSE (0.4301), indicating that it struggled with this dataset. The confusion matrix shows a significant number of false negatives (37), which implies SVM failed to correctly classify many instances in one class.
**Next Steps:** Tuning the **kernel type** (e.g., RBF, polynomial), C parameter (regularization), and gamma (for RBF kernel) could improve performance. SVM may also benefit from **dimensionality reduction** techniques, as it tends to perform better in lower-dimensional spaces.

**7. Extra Trees:**
**Interpretation:** Extra Trees achieved 97.5% accuracy with an RMSE of 0.1581. The confusion matrix indicates only five false negatives, showing that this model performed well, albeit slightly less than Gradient Boosting.
**Next Steps:** Extra Trees can be further tuned using hyperparameters like the **number of trees, depth**, and **minimum samples** per split. It may also benefit from ensemble techniques like **boosting**, or **feature selection** to focus on the most informative features.
**8. AdaBoost:**
**Interpretation:** AdaBoost performed very well, with an accuracy of 98.5% and a low RMSE (0.1225). The confusion matrix shows only three misclassifications, demonstrating AdaBoost's ability to generalize well.
**Next Steps:** Tuning the learning rate and number of estimators could provide further performance boosts. AdaBoost may also benefit from **ensemble techniques** or **cross-validation** to ensure robust generalization across different datasets.

### Further Analysis and Next Steps:
While most models performed exceptionally well, additional techniques could further enhance results:
1. Hyperparameter Tuning:
Fine-tuning model parameters using techniques like **Grid Search** or **Random Search** will likely yield improvements. Parameters like learning rate, depth, number of estimators, and regularization strength could be optimized.
2. Cross-Validation:
While we used a basic train-test split, applying k-fold cross-validation would provide a more reliable estimate of each model’s performance by reducing variance and avoiding overfitting on the test set.
3. Feature Selection and Dimensionality Reduction:
Implementing Principal Component Analysis (PCA) or feature selection methods can help reduce noise, improve computation efficiency, and potentially enhance the predictive power of the models. This is particularly important for models like **KNN** and **SVM**, which can struggle with high-dimensional data.
4. Handling Class Imbalance:
If class imbalance is an issue (though it’s unclear in the current dataset), techniques such as **SMOTE** (Synthetic Minority Over-sampling Technique) or class weighting can be used to balance the dataset and improve model performance on minority classes.

By applying these further techniques, we can continue to refine the model performance, increase predictive accuracy, and reduce error metrics across the board.


