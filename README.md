# EcoDrive Core

**Energy prediction and risk assessment API for EV delivery fleets.**

EcoDrive is a predictive energy intelligence system designed for electric vehicle delivery operations. It forecasts energy consumption per trip, assesses risk before departure, and recommends action — helping fleet operators and drivers avoid unexpected battery depletion, reduce charging downtime, and lower operational costs.

---

## What It Does

Given a trip's parameters, EcoDrive returns:

- Estimated energy consumption (kWh)
- Predicted arrival battery percentage
- Risk score (0.0 – 1.0)
- Risk classification (Low / Medium / High)
- Actionable recommendation (Continue / Optimize route / Charge first)
- Trip feasibility flag

---

## Why It Matters

EV delivery fleets lose time and money when:
- Drivers misjudge battery range in cold weather
- Heavy loads cause unexpected energy drain
- Charging queues create unplanned downtime

EcoDrive makes energy usage predictable before the trip starts — not after the problem occurs.

---

## API

### `POST /predict-energy`

**Request body:**

```json
{
  "distance_km": 60,
  "battery_pct": 50,
  "load_kg": 180,
  "traffic_level": "high",
  "battery_capacity_kwh": 75,
  "temperature_c": 3,
  "regen_efficiency": 0.15,
  "vehicle_type": "van"
}
```

**Response:**

```json
{
  "vehicle_type": "van",
  "distance_km": 60,
  "estimated_kwh": 26.26,
  "arrival_battery_pct": 15.0,
  "risk_score": 0.70,
  "risk": "High",
  "suggestion": "Charge before departure.",
  "trip_feasible": true,
  "inputs": { ... }
}
```

### Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| distance_km | float | ✓ | — | Trip distance in km |
| battery_pct | float | ✓ | — | Current battery % (0–100) |
| load_kg | float | ✓ | — | Cargo weight in kg |
| traffic_level | string | ✓ | — | `low`, `medium`, or `high` |
| battery_capacity_kwh | float | — | 40.0 | Vehicle battery size in kWh |
| temperature_c | float | — | 20.0 | Ambient temperature in °C |
| regen_efficiency | float | — | 0.1 | Regenerative braking efficiency (0–1) |
| vehicle_type | string | — | `van` | `car`, `van`, or `truck` |

---

## Model Features

- **Vehicle-type aware** — separate base consumption rates for car, van, and truck
- **Temperature modeling** — cold weather increases consumption ~1.2% per degree below 20°C
- **Regenerative braking** — savings scale with traffic density
- **Load factor** — heavier cargo increases energy demand
- **Input validation** — rejects invalid inputs with clear error messages
- **Trip feasibility** — explicitly flags trips that cannot be completed on current charge

---

## Getting Started

**Requirements:** Python 3.9+

```bash
git clone https://github.com/UfedoAttah/EcoDrive.git
cd EcoDrive
pip install fastapi uvicorn requests
```

**Run the API:**

```bash
uvicorn main:app --reload
```

**Open interactive docs:**

```
http://127.0.0.1:8000/docs
```

**Run simulation (10 delivery scenarios):**

```bash
python simulate.py
```

---

## Project Structure

```
ecodrive/
  predict.py      # Core energy prediction engine
  main.py         # FastAPI REST API
  simulate.py     # Delivery scenario simulation
  README.md       # This file
```

---

## Roadmap

- [ ] Real fleet data validation against actual consumption
- [ ] Multi-stop route optimization
- [ ] Charging station integration
- [ ] Fleet dashboard (multi-vehicle overview)
- [ ] SECU hardware data integration (sensor-level energy inputs)
- [ ] ML model to replace rule-based prediction engine

---

## Target Market

EV delivery fleets operating in the UK and Europe, particularly last-mile delivery operators managing 10–500 vehicles seeking to reduce energy-related downtime and operational costs.

---

## Status

**v0.2 — Core prediction engine and REST API complete.**  
Active development. Not yet validated against real-world fleet data.

---

*Built as part of the SECU (Smart Energy Control Unit) ecosystem — an intelligent energy routing and management platform for electric vehicles.*
