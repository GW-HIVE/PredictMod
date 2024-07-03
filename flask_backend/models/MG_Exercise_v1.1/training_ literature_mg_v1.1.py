# %%
# Import all necessary packages to run MG ML.
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Load dataset
train_table = pd.read_csv("upsampled_data.csv")
# Split dataset into training (75%) and testing (25%) set
X = train_table.drop(["Status", "Reference"], axis=1)
y = train_table["Status"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=123
)
# Train Random Forest Classifier with dataset
RF = RandomForestClassifier(random_state=123)
RF.fit(X_train, y_train)
#%%
#Convert model into pickle 
#Filename should be as follows: [resource]_[version #].pkl 
model = DTC
filename = "mdclone_v1.1.pkl"
with open(filename, "wb") as fp:
    pickle.dump(model, fp)
fp.close()
#%%
