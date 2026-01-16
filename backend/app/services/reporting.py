def compile_daily_report(events: list[dict]) -> str:
    lines = ["Daily Report"]
    for event in events:
        lines.append(f"- {event.get('market', 'unknown')} ({event.get('score', 0)})")
    return "\n".join(lines)
