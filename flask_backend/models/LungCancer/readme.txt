python -m venv .venv


source .venv/bin/activate
Create requirements.txt with list of libraries
pip install -r requirements.txt
save the model into a pickle file using joblib

created API server as main.python
load model and create HTTP endpoint
create dockerfile
uvicorn main:app --reload --host 127.0.0.1 --port 8080

curl -X POST "http://localhost:8080/predict" -H "Content-Type: application/json" -d @testInput.json

# to start the web service, use the waitress command 
waitress-serve --host=127.0.0.1 --port=8002 app.main:app

curl -X POST http://127.0.0.1:8002/predict -H "Content-Type: application/json" -d "{\"filepath\": \"//Users/diyakb/Documents/GitHub/PredictMod/flask_backend/models/LungCancer/app/backend/gene_expression_data_new.csv\"}"


docker build --no-cache -t lung-cancer-api .

docker run -p 8001:8001 -v "/Users/diyakb/Documents/GitHub/PredictMod/flask_backend/models/LungCancer:/app/host_data" lung-cancer-api

curl -X POST http://127.0.0.1:8001/predict -H "Content-Type: application/json" -d "{\"filepath\": \"/app/host_data/app/backend/gene_expression_data_new.csv\"}"