#%%
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
#%%
df = pd.read_csv("clean_mdclone_v1.1.csv")
df.head()
#%%
X = df.drop(["response"], axis=1)
y = df["response"]
#%%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=123)
DTC = DecisionTreeClassifier(max_depth=5, min_samples_leaf=2, min_samples_split=10, class_weight={0: 1, 1: 3})
DTC.fit(X_train, y_train)
y_pred = DTC.predict(X_test)
print(f'DTC train score: {DTC.score(X_train,y_train)}') #generate a train score - this helps to identify overfitting
print(f'DTC test score:  {DTC.score(X_test,y_test)}') #generate a test score - this helps to identify overfitting 
print(confusion_matrix(y_test, DTC.predict(X_test))) #generate confusion matrix 
print(classification_report(y_test, DTC.predict(X_test))) #generate full classification report (precision, recall, F1)
#%%
#Convert model into pickle 
#Filename should be as follows: [resource]_[version #].pkl 
model = DTC
filename = "mdclone_v1.1.pkl"
with open(filename, "wb") as fp:
    pickle.dump(model, fp)
fp.close()
#%%