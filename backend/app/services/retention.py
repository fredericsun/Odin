from datetime import datetime, timedelta


def cutoff_timestamp(days: int = 7) -> datetime:
    return datetime.utcnow() - timedelta(days=days)
