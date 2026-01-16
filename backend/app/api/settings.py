from fastapi import APIRouter
from sqlmodel import Session, select

from app.db import get_engine, init_db
from app.models import Settings

router = APIRouter()


@router.get("/settings")
def get_settings():
    engine = get_engine()
    init_db(engine)
    with Session(engine) as session:
        return session.exec(select(Settings)).first()


@router.post("/settings")
def update_settings(payload: dict):
    engine = get_engine()
    init_db(engine)
    with Session(engine) as session:
        settings = session.exec(select(Settings)).first()
        for key, value in payload.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        session.add(settings)
        session.commit()
        session.refresh(settings)
        return settings
