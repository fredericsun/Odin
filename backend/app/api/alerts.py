from fastapi import APIRouter
from sqlmodel import Session

from app.db import get_engine, init_db
from app.repository import get_recent_alerts

router = APIRouter()


@router.get("/alerts")
def get_alerts():
    engine = get_engine()
    init_db(engine)
    with Session(engine) as session:
        return get_recent_alerts(session, limit=50)
