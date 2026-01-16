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
