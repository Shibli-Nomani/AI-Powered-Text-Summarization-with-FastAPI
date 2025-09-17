# endpoints/logs.py
from fastapi import APIRouter, HTTPException
from services.logs.metadata_log_server import get_logs  # Direct function import

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/")
async def fetch_all_logs():
    """
    Returns all logged metadata.
    """
    try:
        logs = get_logs()
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Log fetch error: {str(e)}")
