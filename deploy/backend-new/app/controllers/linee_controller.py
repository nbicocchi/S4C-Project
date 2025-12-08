from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from repositories import linee_repo
from core.database import get_db
from schemas.schemas import Linea, LineaCreate
from models.models import Linea as LineaModel

router = APIRouter()

@router.get("/", response_model=list[Linea])
def read_linee(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return linee_repo.get_all(db, skip, limit)

@router.get("/{linea_id}", response_model=Linea)
def read_linea(linea_id: int, db: Session = Depends(get_db)):
    linea = linee_repo.get_by_id(db, linea_id)
    if not linea:
        raise HTTPException(status_code=404, detail="Linea not found")
    return linea

@router.post("/", response_model=Linea)
def create_linea(linea_in: LineaCreate, db: Session = Depends(get_db)):
    linea = LineaModel(**linea_in.dict())
    return linee_repo.create(db, linea)

@router.put("/{linea_id}", response_model=Linea)
def update_linea(linea_id: int, linea_in: LineaCreate, db: Session = Depends(get_db)):
    linea = linee_repo.get_by_id(db, linea_id)
    if not linea:
        raise HTTPException(status_code=404, detail="Linea not found")
    for key, value in linea_in.dict().items():
        setattr(linea, key, value)
    return linee_repo.update(db, linea)

@router.delete("/{linea_id}", response_model=Linea)
def delete_linea(linea_id: int, db: Session = Depends(get_db)):
    linea = linee_repo.get_by_id(db, linea_id)
    if not linea:
        raise HTTPException(status_code=404, detail="Linea not found")
    return linee_repo.delete(db, linea)
