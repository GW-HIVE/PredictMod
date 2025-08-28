import pandas as pd
import numpy as np
import numpy.random as npr

npr.seed(42)

# Define the number of rows and columns
num_rows = 10000  # Get a large number of samples
num_cols = 50  # And a reasonable number of features

feature_names = [f"feature-{f}" for f in range(num_cols)]

# Generate random integers using numpy.random.randint()
# low (inclusive), high (exclusive), size (shape of array)
random_data = np.random.rand(num_rows, num_cols)

# Create a Pandas DataFrame from the random data
df = pd.DataFrame(random_data)
df.columns = feature_names

positive_features = ['feature-0']
negative_features = ['feature-2']
df["Status"] = npr.choice(["R", "NR"], size=num_rows)

responder_indicies = indicies = df["Status"] == "R"
nonresponder_indicies = ~indicies

counts = {str(k): v for k, v in indicies.value_counts().items()}

responder_count = len(responder_indicies == True)

for f in positive_features:
    df.loc[indicies, f] += 0.5 + npr.rand(counts["True"])
    df.loc[~indicies, f] -= 0.5 + npr.rand(counts["False"])
for f in negative_features:
    df.loc[indicies, f] -= 0.5 + npr.rand(counts["True"])
    df.loc[~indicies, f] += 0.5 + npr.rand(counts["False"])

# print(df.loc[indicies].describe())
# print(df.loc[~indicies].describe())

df.to_csv("example_feature_data.csv", index=False)

single_sample = df.sample(n=1)
single_sample.to_csv("example_sample_point.csv", index=False)


