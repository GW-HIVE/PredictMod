import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

import pickle

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

with open("pickled_tree.pickle", "wb") as fp:
    pickle.dump(RF, fp)
fp.close()
