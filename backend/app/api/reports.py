from fastapi import APIRouter
from sqlmodel import Session

from app.db import get_engine, init_db
from app.repository import get_recent_reports

router = APIRouter()


@router.get("/reports")
def get_reports():
    engine = get_engine()
    init_db(engine)
    with Session(engine) as session:
        return get_recent_reports(session, limit=30)
