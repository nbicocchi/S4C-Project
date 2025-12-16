from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import requests

router = APIRouter()


# ======================================================
# Schemi Pydantic
# ======================================================

class PredizioneRequest(BaseModel):
    start_date: str
    num_days: int = 30

# ======================================================
# Predizioni Pedoni
# ======================================================

@router.post("/pedoni")
def api_predizioni_pedoni(payload: PredizioneRequest):
    """
    Restituisce le predizioni pedonali (special=0 e special=1)
    a partire da una data iniziale.
    """
    try:
        start_date = datetime.strptime(payload.start_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato data non valido (YYYY-MM-DD)")

    previsioni = []

    for i in range(payload.num_days):
        date = start_date + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")

        try:
            # special = 0
            resp0 = requests.post(
                "http://prediction:8080/predict",
                json={"date": date_str, "anomaly": 0},
                timeout=10
            )
            resp0.raise_for_status()
            pred0 = resp0.json()

            # special = 1
            resp1 = requests.post(
                "http://prediction:8080/predict",
                json={"date": date_str, "anomaly": 3},
                timeout=10
            )
            resp1.raise_for_status()
            pred1 = resp1.json()

        except requests.RequestException as e:
            raise HTTPException(
                status_code=502,
                detail=f"Errore chiamando pedestrian-prediction: {e}"
            )

        previsioni.append({
            "data": date_str,
            "prediction": pred0,
            "prediction_special": pred1
        })

    return previsioni
