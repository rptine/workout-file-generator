from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta


def pace_str_to_seconds_per_mile(pace: str) -> int:
    """
    pace format: 'M:SS' or 'MM:SS' per mile
    """
    pace = pace.strip()
    parts = pace.split(":")
    if len(parts) != 2:
        raise ValueError(f"Invalid pace '{pace}'. Expected M:SS.")
    minutes = int(parts[0])
    seconds = int(parts[1])
    if seconds < 0 or seconds >= 60:
        raise ValueError(f"Invalid pace '{pace}'. Seconds must be 0-59.")
    return minutes * 60 + seconds


def local_to_utc_iso(date_str: str, time_str: str, tz_offset_hours: int) -> str:
    """
    Converts naive local date+time with a fixed UTC offset into UTC ISO timestamp.
    """
    dt_local = datetime.fromisoformat(f"{date_str}T{time_str}:00")
    tz = timezone(timedelta(hours=tz_offset_hours))
    dt_utc = dt_local.replace(tzinfo=tz).astimezone(timezone.utc)
    return dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")


def mi_to_meters(mi: float) -> float:
    return mi * 1609.344
