from fastapi import FastAPI
from models import models
from core.database import engine

from controllers import (linee_controller, parcheggi_controller, simulazioni_controller)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestione Trasporti e Simulazioni")

app.include_router(linee_controller.router, prefix="/linee", tags=["Linee"])
app.include_router(parcheggi_controller.router, prefix="/parcheggi", tags=["Parcheggi"])
app.include_router(simulazioni_controller.router, prefix="/simulazioni", tags=["Simulazioni"])