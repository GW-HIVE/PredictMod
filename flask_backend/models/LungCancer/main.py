from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from typing import Dict, Any

app = FastAPI(title = "Lung Cancer Prediction API")

#load model file
data = joblib.load('LungCancer_classifier_and_features.pickle')

# Unpack classifier and required feature column names
model = data['classifier']
expected_features = data['features']

# Define flexible request payload (Dictionary matching feature names -> values)
class PredictRequest(BaseModel):
    inputs: Dict[str, Any]

@app.get("/")
def home():
    return {
        "status": "online", 
        "expected_features": expected_features
    }

@app.post("/predict")
def predict(request: PredictRequest):
    try:
        # Convert incoming JSON dict to a pandas DataFrame with exact column ordering
        input_df = pd.DataFrame([request.inputs])[expected_features]
        print("Received input: {input_df.to_dict(orient='records')[0]}")  # Log the received input
        # Ensure all required features are present in the incoming payload
        missing_cols = set(expected_features) - set(input_df.columns)
        if missing_cols:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing feature columns: {list(missing_cols)}"
            )
        
        # Reorder columns to strictly match X.columns from training
        input_df = input_df[expected_features]
        
        # Predict using the extracted Random Forest model
        prediction = model.predict(input_df)
        
        # Optional: Get prediction probabilities if classification
        probability = None
        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(input_df).tolist()

        return {
            "prediction": int(prediction[0]) if hasattr(prediction[0], 'item') else prediction[0],
            "probabilities": probability
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
