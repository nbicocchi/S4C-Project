from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import logging
import numpy as np
from datetime import datetime

LOG = logging.getLogger('uvicorn.info')

try:
    model = joblib.load("model/mobility_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    label_encoder = joblib.load("model/label_encoder.pkl")
    LOG.info("Model, scaler, encoder loaded.")
except Exception as e:
    print("Errore nel caricamento del modello o dei preprocessori:", e)

class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"

class MobilityRequest(BaseModel):
    date: str  # formato: 'YYYY-MM-DD'
    layerid: str  # ID geografico ACE come stringa

# Istanza dell'app FastAPI
app = FastAPI()

@app.get("/health")

def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")

@app.post("/predict")
def predict_mobility(req: MobilityRequest):
    try:
        # Conversione della data in datetime
        date_obj = datetime.strptime(req.date, "%Y-%m-%d")

        # Creazione delle feature derivate
        weekday = date_obj.weekday()
        week = date_obj.isocalendar().week - 35  # adatta il min come nel training (es: week.min = 35)
        weekend = 1 if weekday in [5, 6] else 0
        date_int = int(date_obj.timestamp() * 1e9)  # int64 formato timestamp simile a quello nel dataset

        # Encoding layerid come fatto nel training
        encoded_layerid = label_encoder.transform([req.layerid])[0]

        # Creazione del DataFrame in input con tutte le feature originali
        X = pd.DataFrame([{
            "date": date_int,
            "layerid": encoded_layerid,
            "weekday": weekday,
            "week": week,
            "weekend": weekend
        }])

        # Scaling
        X_scaled = scaler.transform(X)

        # Predizione logaritmica
        y_log_pred = model.predict(X_scaled)

        # Inverso del log1p usato nel training
        y_pred = np.expm1(y_log_pred)

        return {"prediction": float(y_pred[0])}

    except Exception as e:
        LOG.info("Errore durante la predizione:", e)
        return {"error": str(e)}
