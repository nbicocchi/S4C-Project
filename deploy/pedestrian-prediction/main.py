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
    special: int    # 0=normale, 1=giorno top

# FastAPI app instance
app = FastAPI()

@app.get("/health")
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")

@app.post("/predict")
def predict_daily(req: DailyPedestrianRequest):
    try:
        # Parse date and compute day of week
        date_obj = datetime.strptime(req.date, "%Y-%m-%d")
        giorno_settimana = date_obj.weekday()  # 0=Monday, 6=Sunday
        mese = date_obj.month
        giorno_mese = date_obj.day

        # Prepare DataFrame for model
        X = pd.DataFrame([{
            "giorno_settimana": giorno_settimana,
            "mese": mese,
            "giorno_mese": giorno_mese,
            "Special": req.special
        }])

        # Make prediction
        y_pred = model.predict(X)

        return {"prediction": float(y_pred[0])}

    except Exception as e:
        return {"error": str(e)}
