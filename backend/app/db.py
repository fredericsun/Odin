from sqlmodel import SQLModel, Session, create_engine, select

from app.config import get_settings
from app.models import Settings


def get_engine():
    settings = get_settings()
    return create_engine(settings.database_url, echo=False)


def init_db(engine) -> None:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        existing = session.exec(select(Settings)).first()
        if existing is None:
            session.add(Settings())
            session.commit()
