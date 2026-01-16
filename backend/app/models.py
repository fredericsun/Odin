from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Settings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    odds_jump_abs: float = 0.05
    odds_jump_pctile: float = 0.99
    volume_spike_abs: float = 1000.0
    liquidity_spike_abs: float = 5000.0
    alert_cooldown_minutes: int = 30
    report_hour_local: int = 7
    max_position_usd: float = 100.0
    market_scope: str = "top_50_liquidity"


class MarketSnapshot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    market_id: Optional[str] = None
    asset_id: Optional[str] = None
    odds: float = 0.0
    volume: float = 0.0
    liquidity: float = 0.0
    observed_at: datetime = Field(default_factory=datetime.utcnow)


class MarketEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    market_id: Optional[str] = None
    asset_id: Optional[str] = None
    triggered: str
    odds: float = 0.0
    volume: float = 0.0
    liquidity: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Alert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: Optional[int] = None
    asset_id: Optional[str] = None
    status: str = "sent"
    subject: str = ""
    body: str = ""
    sent_at: datetime = Field(default_factory=datetime.utcnow)


class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    report_date: date
    subject: str = ""
    body: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
