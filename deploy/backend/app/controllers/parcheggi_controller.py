from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from repositories import parcheggi_repo
from core.database import get_db
from schemas.schemas import Parcheggio, ParcheggioCreate
from models.models import Parcheggio as ParcheggioModel

router = APIRouter()

@router.get("/", response_model=list[Parcheggio])
def read_parcheggi(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return parcheggi_repo.get_all(db, skip, limit)

@router.get("/{parcheggio_id}", response_model=Parcheggio)
def read_parcheggio(parcheggio_id: int, db: Session = Depends(get_db)):
    parcheggio = parcheggi_repo.get_by_id(db, parcheggio_id)
    if not parcheggio:
        raise HTTPException(status_code=404, detail="Parcheggio not found")
    return parcheggio

@router.post("/", response_model=Parcheggio)
def create_parcheggio(parcheggio_in: ParcheggioCreate, db: Session = Depends(get_db)):
    parcheggio = ParcheggioModel(**parcheggio_in.dict())
    return parcheggi_repo.create(db, parcheggio)

@router.put("/{parcheggio_id}", response_model=Parcheggio)
def update_parcheggio(parcheggio_id: int, parcheggio_in: ParcheggioCreate, db: Session = Depends(get_db)):
    parcheggio = parcheggi_repo.get_by_id(db, parcheggio_id)
    if not parcheggio:
        raise HTTPException(status_code=404, detail="Parcheggio not found")
    for key, value in parcheggio_in.dict().items():
        setattr(parcheggio, key, value)
    return parcheggi_repo.update(db, parcheggio)

@router.delete("/{parcheggio_id}", response_model=Parcheggio)
def delete_parcheggio(parcheggio_id: int, db: Session = Depends(get_db)):
    parcheggio = parcheggi_repo.get_by_id(db, parcheggio_id)
    if not parcheggio:
        raise HTTPException(status_code=404, detail="Parcheggio not found")
    return parcheggi_repo.delete(db, parcheggio)
