from sqlalchemy.orm import Session
from models.models import Linea

def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Linea).offset(skip).limit(limit).all()

def get_by_id(db: Session, linea_id: int):
    return db.query(Linea).filter(Linea.id == linea_id).first()

def create(db: Session, linea: Linea):
    db.add(linea)
    db.commit()
    db.refresh(linea)
    return linea

def update(db: Session, linea: Linea):
    db.commit()
    db.refresh(linea)
    return linea

def delete(db: Session, linea: Linea):
    db.delete(linea)
    db.commit()
    return linea
