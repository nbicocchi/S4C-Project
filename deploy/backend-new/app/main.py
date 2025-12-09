from fastapi import FastAPI
from models import models
from core.database import engine

from controllers import (linee_controller, parcheggi_controller, simulazioni_controller, health_controller, mappa_controller)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestione Trasporti e Simulazioni")

app.include_router(linee_controller.router, prefix="/linee", tags=["Linee"])
app.include_router(parcheggi_controller.router, prefix="/parcheggi", tags=["Parcheggi"])
app.include_router(simulazioni_controller.router, prefix="/simulazioni", tags=["Simulazioni"])
app.include_router(mappa_controller.router, prefix="/map", tags=["Map"])
app.include_router(health_controller.router, prefix="/health", tags=["Health"])

# Run directly with uvicorn if needed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080
    )
