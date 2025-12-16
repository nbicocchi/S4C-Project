from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime
import logging

LOG = logging.getLogger("uvicorn.info")

# Load model
try:
    model = joblib.load("model/pedestrians_model.pkl")
    LOG.info("Model loaded.")
except Exception as e:
    LOG.error("Errore nel caricamento del modello o dei preprocessori: %s", e)

# Response model for health check
class HealthCheck(BaseModel):
    status: str = "OK"

# Request model for prediction
class DailyPedestrianRequest(BaseModel):
    date: str       # format: YYYY-MM-DD
    anomaly: int    # 0=normale, 3=giorno top

# FastAPI app instance
app = FastAPI()

def predict_for_day(date_str: str, anomaly: int) -> float:
    # Parse date and compute day of week
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    giorno_settimana = date_obj.weekday()  # 0=Monday, 6=Sunday
    mese = date_obj.month
    giorno_mese = date_obj.day

    # Prepare DataFrame for model
    X = pd.DataFrame([{
        "giorno_settimana": giorno_settimana,
        "mese": mese,
        "anomalia": anomaly
    }])

    y_pred = model.predict(X)

    return float(y_pred[0])

@app.get("/health")
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")

@app.post("/predict")
def predict_daily(req: DailyPedestrianRequest):
    try:
        daily_prediction = predict_for_day(req.date, req.anomaly)
        return daily_prediction
    except Exception as e:
        return {"error": str(e)}
