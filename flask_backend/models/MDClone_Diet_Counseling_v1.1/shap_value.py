#%%
import pickle
import pandas as pd
import shap
import pandas as pd
import shap
import pickle
#%%
# Open model 
filename = "MDClone_DTCv1.2.pickle"
with open(filename, "rb") as fp:
    model = pickle.load(fp)

# Upload a single patient's data 
sample = pd.read_csv("MDClone_unknown2.csv")

# Generate Shapely Force Plot 
explainer = shap.Explainer(model)
shap_values = explainer.shap_values(sample)
shap.plots.force(explainer.expected_value[0], shap_values[0][0,:], sample.iloc[0,:],matplotlib=True)
# %%
