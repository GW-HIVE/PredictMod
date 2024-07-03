import pandas as pd
import pickle

with open("pickled_tree.pickle", "rb") as fp:
    RF = pickle.load(fp)
fp.close()

# Make predictions from a single patient's data
sample = pd.read_csv("unknown_response.csv")
sample = sample.drop(["Status"], axis=1)
prediction = RF.predict(sample)
print(f"Prediction based on metagenomic profile: {prediction}")
