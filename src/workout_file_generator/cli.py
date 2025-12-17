from __future__ import annotations

import argparse
import os
from typing import Any, Dict, List, Optional

import yaml  # requires pyyaml

from .model import Defaults, Workout
from .util import pace_str_to_seconds_per_mile, local_to_utc_iso, mi_to_meters
from .tcx import write_tcx


def load_config(path: str) -> tuple[Defaults, list[Workout]]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    d = data.get("defaults", {}) or {}
    defaults = Defaults(
        timezone_offset_hours=int(d.get("timezone_offset_hours", -5)),
        sport=str(d.get("sport", "Running")),
        output_dir=str(d.get("output_dir", "out/tcx")),
        start_time=str(d.get("start_time", "12:00")),
        notes_prefix=str(d.get("notes_prefix", "generated workout")),
    )

    workouts: list[Workout] = []
    for w in data.get("workouts", []) or []:
        workouts.append(
            Workout(
                date=str(w["date"]),
                distance_mi=float(w["distance_mi"]),
                pace=str(w["pace"]),
                start_time=str(w.get("start_time")) if w.get("start_time") else None,
                avg_hr=int(w["avg_hr"]) if w.get("avg_hr") is not None else None,
                notes=str(w.get("notes")) if w.get("notes") else None,
            )
        )

    if not workouts:
        raise ValueError("No workouts found in config.")
    return defaults, workouts


def safe_filename(s: str) -> str:
    return "".join(ch for ch in s if ch.isalnum() or ch in ("-", "_", "."))


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate TCX files from simple workout inputs.")
    ap.add_argument("--config", required=True, help="Path to workouts YAML config.")
    args = ap.parse_args()

    defaults, workouts = load_config(args.config)
    os.makedirs(defaults.output_dir, exist_ok=True)

    for w in workouts:
        start_time = w.start_time or defaults.start_time
        start_iso = local_to_utc_iso(w.date, start_time, defaults.timezone_offset_hours)

        pace_s_per_mi = pace_str_to_seconds_per_mile(w.pace)
        duration_s = int(round(w.distance_mi * pace_s_per_mi))

        distance_m = mi_to_meters(w.distance_mi)

        notes_parts = [defaults.notes_prefix]
        if w.notes:
            notes_parts.append(w.notes)
        notes = " - ".join(notes_parts) if notes_parts else None

        fname = safe_filename(f"{w.date}_{start_time.replace(':','')}_{w.distance_mi:.2f}mi_{w.pace.replace(':','')}.tcx")
        out_path = os.path.join(defaults.output_dir, fname)

        write_tcx(
            out_path=out_path,
            sport=defaults.sport,
            start_iso_utc=start_iso,
            duration_s=duration_s,
            distance_m=distance_m,
            avg_hr=w.avg_hr,
            notes=notes,
        )

        print(f"wrote {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
