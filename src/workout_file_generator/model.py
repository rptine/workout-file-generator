from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Defaults:
    timezone_offset_hours: int = -5
    sport: str = "Running"
    output_dir: str = "out/tcx"
    start_time: str = "12:00"
    notes_prefix: str = "generated workout"


@dataclass(frozen=True)
class Workout:
    date: str
    distance_mi: float
    pace: str
    start_time: Optional[str] = None
    avg_hr: Optional[int] = None
    notes: Optional[str] = None
