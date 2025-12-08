from sqlalchemy.orm import Session
from models.models import Parcheggio

def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Parcheggio).offset(skip).limit(limit).all()

def get_by_id(db: Session, parcheggio_id: int):
    return db.query(Parcheggio).filter(Parcheggio.id == parcheggio_id).first()

def create(db: Session, parcheggio: Parcheggio):
    db.add(parcheggio)
    db.commit()
    db.refresh(parcheggio)
    return parcheggio

def update(db: Session, parcheggio: Parcheggio):
    db.commit()
    db.refresh(parcheggio)
    return parcheggio

def delete(db: Session, parcheggio: Parcheggio):
    db.delete(parcheggio)
    db.commit()
    return parcheggio
