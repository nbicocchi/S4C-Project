from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime, date
from calendar import monthrange
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
    special: bool    # 0=normale, 1=giorno top

class MonthlyPedestrianRequest(BaseModel):
    year: int
    month: int

# FastAPI app instance
app = FastAPI()

def predict_for_day(date_str: str, special: bool) -> float:
    # Parse date and compute day of week
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    giorno_settimana = date_obj.weekday()  # 0=Monday, 6=Sunday
    mese = date_obj.month
    giorno_mese = date_obj.day

    # Prepare DataFrame for model
    X = pd.DataFrame([{
        "giorno_settimana": giorno_settimana,
        "mese": mese,
        "giorno_mese": giorno_mese,
        "Special": special
    }])

    # Make prediction
    y_pred = model.predict(X)

    return float(y_pred[0])

@app.get("/health")
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")

@app.post("/predict")
def predict_daily(req: DailyPedestrianRequest):
    try:
        daily_prediction = predict_for_day(req.date, req.special)
        return daily_prediction
    except Exception as e:
        return {"error": str(e)}

@app.post("/predict/month")
def predict_month(req: MonthlyPedestrianRequest):
    year = req.year
    month = req.month

    num_days = monthrange(year, month)[1]

    predictions = []

    for day in range(1, num_days + 1):
        d = date(year, month, day).strftime("%Y-%m-%d")

        predictions.append({
            "data": d,
            "prediction": predict_for_day(d, special=False),
            "prediction_special": predict_for_day(d, special=True)
        })

    return predictions
