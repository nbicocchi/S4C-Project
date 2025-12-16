from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from repositories import simulazioni_repo
from core.database import get_db
from schemas.schemas import Simulazione, SimulazioneCreate, SimulazioneRunRequest, SimulazioneOut
from models.models import Simulazione as SimulazioneModel
from service.simulation_service import run_simulazione
import json, uuid

router = APIRouter()

# --- CRUD endpoints ---

@router.get("/", response_model=list[Simulazione])
def read_simulazioni(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all simulazioni, with optional pagination."""
    return simulazioni_repo.get_all(db, skip, limit)

def safe_load(value, default):
    if value is None:
        return []
    # già dict o list → ok
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            # se dopo il primo loads è ANCORA stringa → doppio JSON
            if isinstance(parsed, str):
                return json.loads(parsed)
            return parsed
        except json.JSONDecodeError:
            return []
    return []

@router.get("/{simulazione_id}", response_model=SimulazioneOut)
def read_simulazione(simulazione_id: str, db: Session = Depends(get_db)):
    """Retrieve a single simulazione by ID."""
    simulazione = simulazioni_repo.get_by_id(db, simulazione_id)
    if not simulazione:
        raise HTTPException(status_code=404, detail="Simulazione not found")
    return {
        "id": simulazione.id,
        "data": simulazione.data,
        "n_turisti": simulazione.n_turisti,
        "timestamp": simulazione.timestamp,

        "risultato": safe_load(simulazione.risultato, {}),
        "parcheggi_usati": safe_load(simulazione.parcheggi_usati, []),
        "linee_usate": safe_load(simulazione.linee_usate, []),
        "parcheggi_esclusi": safe_load(simulazione.parcheggi_esclusi, []),
        "linee_escluse": safe_load(simulazione.linee_escluse, []),
    }

@router.post("/", response_model=Simulazione)
def create_simulazione(simulazione_in: SimulazioneCreate, db: Session = Depends(get_db)):
    """Create a new simulazione."""
    sim_id = simulazione_in.id or str(uuid.uuid4())
    simulazione = SimulazioneModel(
        id=sim_id,
        **simulazione_in.dict(exclude={"id"})
    )
    return simulazioni_repo.create(db, simulazione)

@router.put("/{simulazione_id}", response_model=Simulazione)
def update_simulazione(simulazione_id: str, simulazione_in: SimulazioneCreate, db: Session = Depends(get_db)):
    """Update an existing simulazione by ID."""
    simulazione = simulazioni_repo.get_by_id(db, simulazione_id)
    if not simulazione:
        raise HTTPException(status_code=404, detail="Simulazione not found")
    for key, value in simulazione_in.dict().items():
        setattr(simulazione, key, value)
    return simulazioni_repo.update(db, simulazione)

@router.delete("/{simulazione_id}", response_model=Simulazione)
def delete_simulazione(simulazione_id: str, db: Session = Depends(get_db)):
    """Delete a simulazione by ID."""
    simulazione = simulazioni_repo.get_by_id(db, simulazione_id)
    if not simulazione:
        raise HTTPException(status_code=404, detail="Simulazione not found")
    return simulazioni_repo.delete(db, simulazione)

@router.post("/{simulazione_id}/export")
def export_simulazione(simulazione_id: str, db: Session = Depends(get_db)):
    """
    Export a simulazione as a downloadable JSON file.
    """
    simulazione = simulazioni_repo.get_by_id(db, simulazione_id)
    if not simulazione:
        raise HTTPException(status_code=404, detail="Simulazione not found")

    # Serializzazione sicura tramite schema Pydantic
    export_data = Simulazione.model_validate(simulazione).model_dump()
    return JSONResponse(
        content=export_data,
        headers={
            "Content-Disposition": f'attachment; filename="simulazione_{simulazione_id}.json"'
        }
    )

# --- Run simulation without saving ---
@router.post("/run", response_model=Simulazione)
def api_run_simulazione(
    payload: SimulazioneRunRequest,  # Pydantic model for input
    db: Session = Depends(get_db)
):
    result = run_simulazione(
        db=db,
        data=payload.data,
        n_turisti=payload.n_turisti,
        parcheggi_esclusi_ids=payload.parcheggi_esclusi or [],
        linee_escluse_ids=payload.linee_escluse or []
    )
    return result.model_dump()

