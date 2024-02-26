#%%
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import pickle
print("Ready to Go")
#%%
train_table = pd.read_csv("MDclone_v0.1.csv")
#%%
def numericsex (row):
    ordinalsex = row["sex"]
    if ordinalsex == "Male": return 0
    if ordinalsex == "Female": return 1
    if ordinalsex == "censored": return np.nan
    return ordinalsex
train_table["sex"] = train_table.apply(numericsex, axis =1)
#%%
def numeriethnicity (row):
    ordinalethnicity = row ["ethnicity"]
    if ordinalethnicity == "Not Hispanic or Latino": return 0
    if ordinalethnicity == "Hispanic or Latino": return 1
    if ordinalethnicity == "Unknown by patient": return np.nan
    if ordinalethnicity == "nan": return np.nan
    if ordinalethnicity == "Declined to answer": return np.nan
    if ordinalethnicity == "censored": return np.nan
    return ordinalethnicity
train_table["ethnicity"] = train_table.apply(numeriethnicity, axis=1)
#%%
def numerirace (row): 
    ordinalrace = row ["race"]
    if ordinalrace == "Black or African American": return 0
    if ordinalrace == "White": return 1
    if ordinalrace == "White not of Hispanic origin": return 1
    if ordinalrace == "White  ;  White not of Hispanic origin": return 1
    if ordinalrace == "Native Hawaiian or other Pacific Islander": return 2
    if ordinalrace == "Black or African American  ;  White": return 3 
    if ordinalrace == "Asian": return 2
    if ordinalrace == "Asian  ;  Native Hawaiian or other Pacific Islander": return 2
    if ordinalrace == "Native Hawaiian or other Pacific Islander  ;  White": return 5 
    if ordinalrace == "American Indian or Alaska Native  ;  White": return 6
    if ordinalrace == "American Indian or Alaska Native  ;  Black or African American": return 7
    if ordinalrace == "Black or African American  ;  Native Hawaiian or other Pacific Islander": return 8
    if ordinalrace == "Asian  ;  White": return 9
    if ordinalrace == "Asian  ;  Black or African American": return 10
    if ordinalrace == "American Indian or Alaska Native": return 11
    if ordinalrace == "nan": return np.nan
    if ordinalrace == "Declined to answer": return np.nan
    if ordinalrace == "Declined to answer  ;  White": return np.nan
    if ordinalrace == "Unknown by patient": return np.nan
    if ordinalrace == "Unknown by patient  ;  White": return np.nan
    if ordinalrace == "Black or African American  ;  Unknown by patient": return np.nan
    if ordinalrace == "Declined to answer  ;  White not of Hispanic origin": return np.nan
    if ordinalrace == "Black or African American  ;  Declined to answer": return np.nan
    if ordinalrace == "censored": return np.nan
    return ordinalrace
train_table["race"] = train_table.apply(numerirace, axis=1)
#%%
#Establish X and y variables 
X = train_table.drop(["response"], axis=1)
y = train_table["response"]
print("Table Ready to Go")
#%%
# #Fill missing values with mean
imputer = SimpleImputer(strategy='mean')  
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
#%%
#Train test split
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=0.25 ,random_state=123)
print("Ready to Go")
#%%
#Train Decision Tree Classifier 
DTC = DecisionTreeClassifier() 
DTC.fit(X_train, y_train)
print(f'DTC train score: {DTC.score(X_train,y_train)}')
print(f'DTC test score:  {DTC.score(X_test,y_test)}')
print(confusion_matrix(y_test, DTC.predict(X_test)))
print(classification_report(y_test, DTC.predict(X_test)))
# %%
#Train Support Vector Machine - Just to view performance metrics 
SVM = SVC()
SVM.fit(X_train, y_train)
print(f'SVM train score: {SVM.score(X_train,y_train)}')
print(f'SVM test score:  {SVM.score(X_test,y_test)}')
print(confusion_matrix(y_test, SVM.predict(X_test)))
print(classification_report(y_test, SVM.predict(X_test)))
# %%
#Train Random Forest Classifier - Just to view performance metrics 
RF = RandomForestClassifier() 
RF.fit(X_train, y_train)
print(f'RF train score: {RF.score(X_train,y_train)}')
print(f'RF test score:  {RF.score(X_test,y_test)}')
print(confusion_matrix(y_test, RF.predict(X_test)))
print(classification_report(y_test, RF.predict(X_test)))
# %%
#Convert DTC into pickle 
with open("mdclone_DTC.pickle", "wb") as fp:
    pickle.dump(DTC, fp)
fp.close()
#Open pickle and make a prediction using DTC
with open("mdclone_DTC.pickle", "rb") as fp:
    DTC = pickle.load(fp)
fp.close()
sample = pd.read_csv("MDClone_unknown1.csv")
prediction = DTC.predict(sample)
print(f"Prediction based on EHR data: {prediction}")
