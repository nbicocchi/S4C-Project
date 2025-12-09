from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import logging

LOG = logging.getLogger('uvicorn.info')

try:
    model = joblib.load("model/pedestrians_model.pkl")
    LOG.info("Model loaded.")
except Exception as e:
    print("Errore nel caricamento del modello o dei preprocessori:", e)

class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"

class DailyPedestrianRequest(BaseModel):
    giorno_settimana: int  # 0=Lunedì, 6=Dom
    mese: int              # 1-12
    giorno_mese: int       # 1-31
    Special: int           # 0=normale, 1=giorno top

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
def predict_daily(req: DailyPedestrianRequest):
    try:
        # Converte la richiesta in DataFrame
        X = pd.DataFrame([req.dict()])

        # Predizione
        y_pred = model.predict(X)

        # Restituisci risultato
        return {"predicted_entrate": float(y_pred[0])}

    except Exception as e:
        return {"error": str(e)}