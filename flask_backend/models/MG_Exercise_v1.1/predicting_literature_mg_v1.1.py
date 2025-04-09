#%%
import pickle
import pandas as pd

#%%
# Open the pickle file
filename = "literature_mg.pkl"
with open(filename, "rb") as fp:
    model = pickle.load(fp)

# Upload a single patient's data 
sample = pd.read_csv("unknown_response.csv")

# Make a prediction with the model 
prediction = model.predict(sample)
print(f"Prediction based on EHR: {prediction}")

# Check if the model has feature_importances_ attribute (tree-based models)
if hasattr(model, 'feature_importances_'):
    feature_importances = model.feature_importances_
    feature_names = sample.columns  # assuming sample columns are the feature names
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': feature_importances
    })
    
    # Sort the features by importance and get the top 10
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False).head(10)
    
    print("\nTop 10 Features by Importance:")
    print(feature_importance_df)
else:
    print("The model does not support feature importance extraction.")
