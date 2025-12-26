from __future__ import annotations

from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET
from typing import Optional


GARMIN_NS = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"


def write_tcx(
    *,
    out_path: str,
    sport: str,
    start_iso_utc: str,
    duration_s: int,
    distance_m: float,
    avg_hr: Optional[int],
    notes: Optional[str],
) -> None:
    ET.register_namespace("", GARMIN_NS)
    ET.register_namespace("xsi", XSI_NS)

    root = ET.Element(f"{{{GARMIN_NS}}}TrainingCenterDatabase", attrib={
        f"{{{XSI_NS}}}schemaLocation":
            f"{GARMIN_NS} http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd"
    })

    activities = ET.SubElement(root, f"{{{GARMIN_NS}}}Activities")
    activity = ET.SubElement(activities, f"{{{GARMIN_NS}}}Activity", attrib={"Sport": sport})
    ET.SubElement(activity, f"{{{GARMIN_NS}}}Id").text = start_iso_utc

    lap = ET.SubElement(activity, f"{{{GARMIN_NS}}}Lap", attrib={"StartTime": start_iso_utc})
    ET.SubElement(lap, f"{{{GARMIN_NS}}}TotalTimeSeconds").text = str(duration_s)
    ET.SubElement(lap, f"{{{GARMIN_NS}}}DistanceMeters").text = f"{distance_m:.2f}"

    if avg_hr is not None:
        avg = ET.SubElement(lap, f"{{{GARMIN_NS}}}AverageHeartRateBpm")
        ET.SubElement(avg, f"{{{GARMIN_NS}}}Value").text = str(avg_hr)

    ET.SubElement(lap, f"{{{GARMIN_NS}}}Intensity").text = "Active"
    ET.SubElement(lap, f"{{{GARMIN_NS}}}TriggerMethod").text = "Manual"

    # Trackpoints: start and end (minimal viable TCX)
    track = ET.SubElement(lap, f"{{{GARMIN_NS}}}Track")
    tp1 = ET.SubElement(track, f"{{{GARMIN_NS}}}Trackpoint")
    ET.SubElement(tp1, f"{{{GARMIN_NS}}}Time").text = start_iso_utc

    start_dt = datetime.strptime(start_iso_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    end_dt = start_dt + timedelta(seconds=duration_s)
    end_iso = end_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    tp2 = ET.SubElement(track, f"{{{GARMIN_NS}}}Trackpoint")
    ET.SubElement(tp2, f"{{{GARMIN_NS}}}Time").text = end_iso
    ET.SubElement(tp2, f"{{{GARMIN_NS}}}DistanceMeters").text = f"{distance_m:.2f}"

    if notes:
        ET.SubElement(activity, f"{{{GARMIN_NS}}}Notes").text = notes

    tree = ET.ElementTree(root)
    tree.write(out_path, encoding="utf-8", xml_declaration=True)
