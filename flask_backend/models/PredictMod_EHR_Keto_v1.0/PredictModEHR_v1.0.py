#%%
import pickle
import pandas as pd
#%%
#Make a prediction using SVM
with open("svm_classifier.pkl", "rb") as fp:
    SVM = pickle.load(fp)
fp.close()

# Make predictions from a single patient's data - Using MDClone sample given we do not have access to Cosmos data. 
sample = pd.read_csv("MDClone_unknown1.csv")
sample = sample.drop(["response"], axis=1)
prediction = SVM.predict(sample)
print(f"Prediction based on EHR data: {prediction}")
