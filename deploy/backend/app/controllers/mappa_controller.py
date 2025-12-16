# mappa_controller.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.database import get_db
from utils.geoutils import to_float
from schemas.schemas import Parcheggio, Linea
from repositories import parcheggi_repo, linee_repo

router = APIRouter()

# ======================= Helpers =======================
def safe_int(val, default=0):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def safe_float(val, default=0.0):
    try:
        return to_float(val)
    except (ValueError, TypeError):
        return default

@router.get("/")
def api_mappa_dati(db: Session = Depends(get_db)):
    """
    Returns active parking spots and transport lines with lat/lng as floats.
    """
    try:
        # Load and filter active parcheggi and linee
        parcheggi = [
            Parcheggio.model_validate(p).model_dump()
            for p in parcheggi_repo.get_all(db, skip=0, limit=1000)
        ]

        linee = [
            Linea.model_validate(l).model_dump()
            for l in linee_repo.get_all(db, skip=0, limit=1000)
        ]
        # Convert coordinates to float
        for p in parcheggi:
            p["latitudine"] = safe_float(p["latitudine"])
            p["longitudine"] = safe_float(p["longitudine"])

        for l in linee:
            for campo in ["partenza_lat", "partenza_lng", "arrivo_lat", "arrivo_lng"]:
                l[campo] = safe_float(l[campo])

        return JSONResponse(content={"parcheggi": parcheggi, "linee_trasporto": linee})

    except Exception as e:
        # Log the error and return 500
        print("Errore mappa:", e)
        raise HTTPException(status_code=500, detail=str(e))
