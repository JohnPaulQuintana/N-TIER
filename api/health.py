from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/health",
    tags=["Server Status"],
)

@router.get("/status")
def health_check():
    return {
        "status": "ok",
        "message": "Car airconditioning backend is running",
    }