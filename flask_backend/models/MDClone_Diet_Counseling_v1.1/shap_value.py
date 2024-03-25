#%%
import pickle
import pandas as pd
import shap
import pandas as pd
import shap
import pickle
#%%
# Open model 
<<<<<<< HEAD
filename = "MDClone_DTCv1.2.pickle"
=======
filename = "mdclonev1.1.pickle"
>>>>>>> 029c027e (Continue model refactor into the backend)
with open(filename, "rb") as fp:
    model = pickle.load(fp)

# Upload a single patient's data 
<<<<<<< HEAD
sample = pd.read_csv("MDClone_unknown2.csv")
=======
sample = pd.read_csv("MDClone_unknown1.csv")
>>>>>>> 029c027e (Continue model refactor into the backend)

# Generate Shapely Force Plot 
explainer = shap.Explainer(model)
shap_values = explainer.shap_values(sample)
<<<<<<< HEAD
shap.plots.force(explainer.expected_value[0], shap_values[0][0,:], sample.iloc[0,:],matplotlib=True)
# %%
=======
instance_idx = 0  # Assuming you want to explain the first instance in the sample data
shap.force_plot(explainer.expected_value, shap_values[instance_idx], sample.iloc[instance_idx], matplotlib=True)
>>>>>>> 029c027e (Continue model refactor into the backend)
