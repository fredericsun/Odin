from fastapi import APIRouter

router = APIRouter()


@router.get("/alerts")
def get_alerts():
    return []
