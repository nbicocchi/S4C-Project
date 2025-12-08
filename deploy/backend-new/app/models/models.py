from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from core.database import Base

class Linea(Base):
    __tablename__ = "linee"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    comune_partenza = Column(String, nullable=False)
    partenza_lat = Column(Float)
    partenza_lng = Column(Float)
    comune_arrivo = Column(String, nullable=False)
    arrivo_lat = Column(Float)
    arrivo_lng = Column(Float)
    capienza = Column(Integer)
    attiva = Column(Boolean)
    sabato = Column(Boolean)
    domenica = Column(Boolean)
    frequenza_giornaliera = Column(Float)

class Parcheggio(Base):
    __tablename__ = "parcheggi"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    comune = Column(String, nullable=False)
    capienza = Column(Integer, nullable=False)
    attivo = Column(Boolean, nullable=False)
    latitudine = Column(Float, nullable=False)
    longitudine = Column(Float, nullable=False)

class Simulazione(Base):
    __tablename__ = "simulazioni"
    id = Column(String, primary_key=True, index=True)
    data = Column(String, nullable=False)
    n_turisti = Column(Integer, nullable=False)
    risultato = Column(Text)
    parcheggi_usati = Column(Text)
    linee_usate = Column(Text)
    parcheggi_esclusi = Column(Text)
    linee_escluse = Column(Text)
    timestamp = Column(String)
