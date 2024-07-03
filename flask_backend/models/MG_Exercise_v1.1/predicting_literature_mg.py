#%%
import pickle
import pandas as pd
#%%
#Open the pickle
filename = "literature_mg.pkl"
with open(filename, "rb") as fp:
    model = pickle.load(fp)
fp.close()

# Upload a single patients data 
sample = pd.read_csv("unknown_response.csv")
# sample = sample.drop(["response"], axis=1)
#Make a prediction with model 
prediction = model.predict(sample)
print(f"Prediction based on EHR: {prediction}")
