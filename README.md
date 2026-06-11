# 🚗 IoT Vehicle Tracking & Geofence Threat Prevention System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![ThingSpeak](https://img.shields.io/badge/Cloud-ThingSpeak-orange?logo=mathworks)
![MATLAB](https://img.shields.io/badge/Viz-MATLAB%20Analytics-red?logo=mathworks)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

A **fully operational, end-to-end IoT system** that simulates a vehicle's real-time movement, enforces geofence boundary rules using high-precision Haversine geometry, streams live telemetry to the cloud, and auto-generates executive PDF reports — all from a local Python digital twin engine.

---

## 📌 Table of Contents

- [System Overview](#-system-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Directory Structure](#-directory-structure)
- [Features](#-features)
- [Cloud Dashboard](#-cloud-dashboard)
- [Setup & Installation](#-setup--installation)
- [Usage](#-usage)
- [Geofence Logic](#-geofence-logic)
- [ThingSpeak Channel Configuration](#-thingspeak-channel-configuration)
- [Sample Output](#-sample-output)
- [Portfolio Notes](#-portfolio-notes)

---

## 🧭 System Overview

This project implements a **hybrid local/cloud IoT architecture** designed around a real-world vehicle tracking use case. A Python-based deterministic digital twin simulates vehicle GPS movement along a predefined route. At each simulation tick:

1. The vehicle's position is evaluated against a **50-metre geofence** centred on Home Base (New Delhi, India).
2. A **status code** is computed (Safe / Warning / Breach).
3. Telemetry is published to **ThingSpeak** via HTTP API (Latitude, Longitude, Speed, Status).
4. Data is **appended to a local CSV** for persistent history.
5. An **executive PDF report** is auto-generated summarising the full route and incident log.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              LOCAL LAYER (Python)                   │
│                                                     │
│  simulation_engine.py                               │
│  ├── Digital Twin (deterministic route engine)      │
│  ├── Haversine Geofence (50m radius, New Delhi)     │
│  ├── CSV Logger (append mode)                       │
│  └── PDF Report Generator                          │
└──────────────────┬──────────────────────────────────┘
                   │  HTTP POST (ThingSpeak API)
                   ▼
┌─────────────────────────────────────────────────────┐
│              CLOUD LAYER (ThingSpeak)               │
│                                                     │
│  Channel 3405582                                    │
│  ├── Field 1: Latitude                              │
│  ├── Field 2: Longitude                             │
│  ├── Field 3: Speed (km/h)                          │
│  └── Field 4: Status Code                          │
│                                                     │
│  MATLAB Visualisations                              │
│  ├── Widget 1: Speed Gauge (0–115 km/h)             │
│  └── Widget 2: Web GIS Map (live satellite tiles)  │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Simulation Engine | Python 3.10+ |
| Geofence Algorithm | Haversine Formula (custom implementation) |
| Cloud IoT Platform | ThingSpeak (MathWorks) |
| Cloud Visualisation | MATLAB Analytics — Gauge + Web GIS Map |
| Data Persistence | CSV (append mode) |
| Reporting | Auto-generated PDF |
| Version Control | Git / GitHub |

---

## 📂 Directory Structure

```
iot-vehicle-tracker/
├── .gitignore                          # Protects secrets & build artefacts
├── README.md                           # This file
├── python_simulation/
│   └── simulation_engine.py            # Core digital twin & geofence engine
├── data/
│   └── location_history.csv            # Persistent telemetry log (append mode)
├── outputs/
│   └── reports/
│       └── route_incident_report.pdf   # Auto-generated executive route report
└── dashboard/                          # ⚠️ LOCAL ONLY — git-ignored, never committed
    └── config.json                     # ThingSpeak API key & channel config (secret)
```

> 🔒 The `dashboard/` folder exists locally but is excluded from this repository via `.gitignore`. It must be created manually after cloning — see [Setup & Installation](#-setup--installation).

---

## ✨ Features

**Local / Python**
- Deterministic digital twin simulates realistic vehicle movement tick-by-tick
- High-precision Haversine geofence with a 50-metre radius boundary
- Three-level status classification: `SAFE` · `WARNING` · `BREACH`
- Append-mode CSV logger — zero data loss across multiple runs
- Auto-generated PDF executive report with route summary and incident table

**Cloud / ThingSpeak**
- Live 4-field telemetry channel publishing Lat, Lng, Speed, and Status
- MATLAB Speed Gauge widget scaled to 115 km/h
- Custom MATLAB Web GIS Map using a `webread` JSON fetch to pull the latest coordinates directly from the ThingSpeak API, rendering real-time high-resolution satellite tiles at the correct latitude band (~28°45′10″N)

---

## 📊 Cloud Dashboard

| Widget | Type | Description |
|---|---|---|
| Vehicle Speed Gauge | MATLAB Gauge | Real-time speed display, 0–115 km/h range |
| Live GIS Map | MATLAB Web Map | Satellite tile map, auto-centred on latest GPS fix |

The GIS map widget uses a raw `webread` call to the ThingSpeak JSON API, bypassing standard platform wrappers to render the most recently published coordinates at full satellite resolution.

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10 or higher
- A ThingSpeak account with an active channel (see [ThingSpeak Channel Configuration](#-thingspeak-channel-configuration))
- `pip` package manager

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/iot-vehicle-tracker.git
cd iot-vehicle-tracker
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Credentials

Create `dashboard/config.json` locally (this file is git-ignored and must **never** be committed):

```json
{
  "thingspeak_write_api_key": "YOUR_WRITE_API_KEY_HERE",
  "channel_id": "3405582"
}
```

> ⚠️ **Security notice:** `dashboard/config.json` contains your ThingSpeak Write API key and is explicitly excluded from version control via `.gitignore`. The `dashboard/` folder is local-only and does not appear in this repository. If you fork or clone this project, you must create this file manually with your own credentials. Never commit API keys to any public or private repository.

---

## 🚀 Usage

Run the simulation engine from the project root:

```bash
python python_simulation/simulation_engine.py
```

The engine will:
1. Simulate the vehicle route tick-by-tick
2. Evaluate geofence status at each position
3. Publish telemetry to ThingSpeak
4. Append each record to `data/location_history.csv`
5. Generate `outputs/reports/route_incident_report.pdf` on completion

---

## 🔵 Geofence Logic

The geofence is implemented using the **Haversine formula**, which calculates the great-circle distance between two GPS coordinates on a sphere.

**Home Base:** `Lat 28.6139°N, Lng 77.2090°E` (New Delhi, India)
**Radius:** `50 metres`

The 50-metre radius defines the **safe zone** — the vehicle is expected to remain inside it. Crossing outside the boundary is the threat condition.

| State Code | Status Variable | Condition | Description |
|---|---|---|---|
| `1` | `SAFE_ZONE` | Distance **< 50m** | Vehicle inside home base perimeter — normal state |
| `3` | `BREACH_ALERT` | Distance **≥ 50m** | Vehicle has left the safe zone — theft/escape alert triggered |

> ℹ️ State codes are published to ThingSpeak **Field 4** as integers (`1` or `3`). The string labels `SAFE_ZONE` and `BREACH_ALERT` are used internally in `simulation_engine.py` and logged to the CSV.

---

## 📡 ThingSpeak Channel Configuration

| Setting | Value |
|---|---|
| Channel ID | `3405582` |
| Field 1 | Latitude |
| Field 2 | Longitude |
| Field 3 | Speed (km/h) |
| Field 4 | State Code (`1` = SAFE_ZONE, `3` = BREACH_ALERT) |

API endpoint used for publishing:
```
https://api.thingspeak.com/update?api_key=<WRITE_KEY>&field1=<LAT>&field2=<LNG>&field3=<SPEED>&field4=<STATUS>
```

---

## 📄 Sample Output

**CSV Log (`data/location_history.csv`):**

```
timestamp,latitude,longitude,speed_kmh,status,state_code,distance_from_base_m
2025-01-15 10:00:01,28.6135,77.2085,42.3,SAFE_ZONE,1,62.4
2025-01-15 10:00:06,28.6141,77.2097,38.7,BREACH_ALERT,3,84.1
2025-01-15 10:00:11,28.6139,77.2090,12.1,SAFE_ZONE,1,0.5
```

**PDF Report** auto-generated at `outputs/reports/route_incident_report.pdf` — includes route summary statistics, geofence event log, and max/min/average speed figures.

---

## 🏆 Portfolio Notes

This project demonstrates:

- **IoT System Design** — end-to-end data pipeline from sensor simulation to cloud dashboard
- **Geospatial Engineering** — Haversine formula applied to real-world boundary detection
- **Cloud Integration** — ThingSpeak HTTP API, MATLAB visualisation scripting
- **Data Engineering** — persistent CSV logging, structured PDF report generation
- **DevOps Hygiene** — `.gitignore` secret management with explicit exclusion of `dashboard/config.json`, clean repo structure, production-grade documentation; API key rotation applied after accidental early exposure

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

*Built with Python · ThingSpeak · MATLAB · Haversine Geometry*