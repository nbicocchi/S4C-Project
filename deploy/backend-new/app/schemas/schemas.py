from pydantic import BaseModel
from typing import List, Optional

# ---------------- Linea ----------------
class LineaBase(BaseModel):
    nome: str
    comune_partenza: str
    partenza_lat: Optional[float]
    partenza_lng: Optional[float]
    comune_arrivo: str
    arrivo_lat: Optional[float]
    arrivo_lng: Optional[float]
    capienza: Optional[int]
    attiva: Optional[bool]
    sabato: Optional[bool]
    domenica: Optional[bool]
    frequenza_giornaliera: Optional[float]

class LineaCreate(LineaBase):
    pass

class Linea(LineaBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode

# ---------------- Parcheggio ----------------
class ParcheggioBase(BaseModel):
    nome: str
    comune: str
    capienza: int
    attivo: bool
    latitudine: float
    longitudine: float

class ParcheggioCreate(ParcheggioBase):
    pass

class Parcheggio(ParcheggioBase):
    id: int

    class Config:
        from_attributes = True

# ---------------- Simulazione ----------------
class SimulazioneBase(BaseModel):
    id: str
    data: str
    n_turisti: int
    risultato: Optional[str] = None
    parcheggi_usati: Optional[str] = None
    linee_usate: Optional[str] = None
    parcheggi_esclusi: Optional[str] = None
    linee_escluse: Optional[str] = None
    timestamp: Optional[str] = None

class SimulazioneCreate(SimulazioneBase):
    pass

class Simulazione(SimulazioneBase):

    class Config:
        from_attributes = True

class SimulazioneRunRequest(BaseModel):
    data: str
    n_turisti: int
    parcheggi_esclusi: Optional[List[int]] = []
    linee_escluse: Optional[List[int]] = []
