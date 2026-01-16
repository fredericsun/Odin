from collections import deque
from typing import Optional


class RingBuffer:
    def __init__(self, maxlen: int = 120):
        self._data = deque(maxlen=maxlen)

    def append(self, snapshot: dict) -> None:
        self._data.append(snapshot)

    def last(self) -> Optional[dict]:
        return self._data[-1] if self._data else None

    def values(self) -> list[dict]:
        return list(self._data)


class SignalEngine:
    def __init__(self, odds_jump_abs: float):
        self.odds_jump_abs = odds_jump_abs

    def detect(self, buffer: RingBuffer, current: dict) -> Optional[dict]:
        triggered = []
        last = buffer.last()
        if last:
            if abs(current["odds"] - last["odds"]) >= self.odds_jump_abs:
                triggered.append("odds_jump_abs")
        if not triggered:
            return None
        return {"triggered": triggered, "current": current}
