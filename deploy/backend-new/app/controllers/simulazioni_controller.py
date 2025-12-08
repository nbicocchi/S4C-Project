from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from repositories import simulazioni_repo
from core.database import get_db
from schemas.schemas import Simulazione, SimulazioneCreate, SimulazioneRunRequest
from models.models import Simulazione as SimulazioneModel
from service.simulation_service import run_simulazione

router = APIRouter()

# --- CRUD endpoints ---

@router.get("/", response_model=list[Simulazione])
def read_simulazioni(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all simulazioni, with optional pagination."""
    return simulazioni_repo.get_all(db, skip, limit)

@router.get("/{simulazione_id}", response_model=Simulazione)
def read_simulazione(simulazione_id: str, db: Session = Depends(get_db)):
    """Retrieve a single simulazione by ID."""
    simulazione = simulazioni_repo.get_by_id(db, simulazione_id)
    if not simulazione:
        raise HTTPException(status_code=404, detail="Simulazione not found")
    return simulazione

@router.post("/", response_model=Simulazione)
def create_simulazione(simulazione_in: SimulazioneCreate, db: Session = Depends(get_db)):
    """Create a new simulazione."""
    simulazione = SimulazioneModel(**simulazione_in.dict())
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

# --- Run simulation without saving ---
@router.post("/run", response_model=Simulazione)
def api_run_simulazione(
    payload: SimulazioneRunRequest,  # Pydantic model for input
    db: Session = Depends(get_db)
):
    # Call your simulation function
    return run_simulazione(
        db=db,
        data=payload.data,
        n_turisti=payload.n_turisti,
        parcheggi_esclusi_ids=payload.parcheggi_esclusi or [],
        linee_escluse_ids=payload.linee_escluse or []
    )

