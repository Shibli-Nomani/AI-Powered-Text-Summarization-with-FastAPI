from fastapi import APIRouter

# 👨‍⚕️ Router for Health Check
router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("/")
async def health_check():
    """
    Simple health check to verify the service is running.
    """
    return {
        "status": "ok",
        "service": "multi-agent system"
    }
