from sqlalchemy.orm import Session
from models.models import Simulazione

def get_all(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of simulazioni with optional pagination."""
    return db.query(Simulazione).offset(skip).limit(limit).all()

def get_by_id(db: Session, simulazione_id: str):
    """Retrieve a single simulazione by its ID."""
    return db.query(Simulazione).filter(Simulazione.id == simulazione_id).first()

def create(db: Session, simulazione: Simulazione):
    """Create a new simulazione record."""
    db.add(simulazione)
    db.commit()
    db.refresh(simulazione)
    return simulazione

def update(db: Session, simulazione: Simulazione):
    """Update an existing simulazione record."""
    db.commit()
    db.refresh(simulazione)
    return simulazione

def delete(db: Session, simulazione: Simulazione):
    """Delete a simulazione record."""
    db.delete(simulazione)
    db.commit()
    return simulazione
