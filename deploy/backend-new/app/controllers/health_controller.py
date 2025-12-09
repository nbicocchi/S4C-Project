from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    """
    Simple health check endpoint.
    Returns a JSON with status 'ok'.
    """
    return {"status": "ok"}
