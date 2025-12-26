# workout-file-generator

Generate `.tcx` workout files from minimal inputs (date, distance, pace).

This tool is useful for creating lightweight workouts that can be imported into fitness platforms like COROS or Strava for testing training load, daily mileage, or calendar attribution.

---

## setup

Create and activate a virtual environment, then install the package in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## usage (workouts.yaml)

The generator reads workouts from a YAML config file.  
You can start by copying the provided example config and modifying it.

### copy the example config

```bash
cp config/workouts.example.yaml config/workouts.yaml
```

### example `workouts.yaml`

```yaml
timezone_offset_hours: -5
out_dir: out/tcx

workouts:
  - date: 2025-12-10
    distance_mi: 6.5
    pace: "9:14"

  - date: 2025-12-11
    distance_mi: 5.2
    pace: "8:42"

  - date: 2025-12-12
    distance_mi: 5.9
    pace: "8:30"

  - date: 2025-12-13
    distance_mi: 4.3
    pace: "9:53"
```

Each entry in `workouts` generates a separate `.tcx` file.

---

## generate `.tcx` files

Run the CLI with the config file:

```bash
workout-file-generator --config config/workouts.yaml
```

Generated files will be written to the directory specified by `out_dir`.

---

## config fields

### top-level

| field | description |
|------|------------|
| `timezone_offset_hours` | UTC offset for local time (NYC is `-5` in winter, `-4` in summer) |
| `out_dir` | directory where generated `.tcx` files will be written |

### workout entries

| field | description |
|------|------------|
| `date` | workout date in `YYYY-MM-DD` format |
| `distance_mi` | distance in miles (decimals allowed) |
| `pace` | target pace in `M:SS` or `MM:SS` format |

---

## notes

- all timestamps inside the generated `.tcx` files are written in UTC  
- local workout time is derived using `timezone_offset_hours`  
- the tool intentionally avoids silent defaults to prevent incorrect date or time attribution  

---

## license

MIT
