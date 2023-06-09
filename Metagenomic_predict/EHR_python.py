#%%[markdown]
#This is preliminary code for a decision tree classifier (DTC) that can be trained with EHR data from MDClone or Cosmos. - Urnisha Bhuiyan
import pandas as pd 
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
print("Ready to Go")
#%%
train_table = pd.read_csv("ehr_train_table.csv")
print("Table Loaded")
#%%
#Establish X and y variables for Decision Tree Model 
X = train_table.drop(["Response", "Label"], axis=1)
y = train_table["Response"]
#%%
#Split dataset into train and test datasets 
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=0.25 ,random_state=1)
print("Model Ready to Go")
# %%
#Train Decision Tree Model 
DTC = DecisionTreeClassifier()
DTC.fit(X_train,y_train)
print(f'DecisionTreeClassifier train score: {DTC.score(X_train,y_train)}')
print(f'DecisionTreeClassifier test score:  {DTC.score(X_test,y_test)}')
print(confusion_matrix(y_test, DTC.predict(X_test)))
print(classification_report(y_test, DTC.predict(X_test)))