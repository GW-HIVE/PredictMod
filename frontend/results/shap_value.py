#%%
import pickle
import pandas as pd
import shap
import pandas as pd
import shap
import pickle
#%%
# Open model 
filename = "mdclonev1.1.pickle"
with open(filename, "rb") as fp:
    model = pickle.load(fp)

# Upload a single patient's data 
sample = pd.read_csv("MDClone_unknown1.csv")

# Generate Shapely Force Plot 
explainer = shap.Explainer(model)
shap_values = explainer.shap_values(sample)
instance_idx = 0  # Assuming you want to explain the first instance in the sample data
shap.force_plot(explainer.expected_value, shap_values[instance_idx], sample.iloc[instance_idx], matplotlib=True)
