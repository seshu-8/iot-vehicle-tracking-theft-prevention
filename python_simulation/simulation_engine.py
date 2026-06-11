#!/usr/bin/env python3
import os
import json
import time
import math
import random
import csv
from datetime import datetime
import requests

# --- Safely read the Write API Key from our config folder ---
CONFIG_FILE_PATH = os.path.join("..", "dashboard", "config.json")
THINGSPEAK_WRITE_KEY = "XQFPN7O8MVYFXRCZ" # Hardcoded directly to your working channel key

if os.path.exists(CONFIG_FILE_PATH):
    try:
        with open(CONFIG_FILE_PATH, "r") as cfg:
            data = json.load(cfg)
            THINGSPEAK_WRITE_KEY = data.get("thingspeak_write_key", THINGSPEAK_WRITE_KEY)
    except Exception as e:
        print(f"[-] Config read error: {e}")

CSV_DATA_PATH = os.path.join("..", "data", "location_history.csv")
OS_REPORT_DIR = os.path.join("..", "outputs", "reports")
GEOFENCE_RADIUS_METERS = 50.0

# Auto-create data and report folders if missing
os.makedirs(os.path.dirname(CSV_DATA_PATH), exist_ok=True)
os.makedirs(OS_REPORT_DIR, exist_ok=True)

# Starting position centerpoint
HOME_LAT = 28.6139
HOME_LNG = 77.2090

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000.0 
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    return R * (2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a)))

def log_telemetry_to_csv(timestamp, lat, lng, speed, status, alert_type):
    file_exists = os.path.exists(CSV_DATA_PATH)
    with open(CSV_DATA_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Latitude", "Longitude", "Speed_Kmh", "System_Status", "Alert_Type"])
        writer.writerow([timestamp, f"{lat:.6f}", f"{lng:.6f}", f"{speed:.2f}", status, alert_type])

def push_telemetry_to_cloud(lat, lng, speed, state_code):
    url = "https://api.thingspeak.com/update"
    payload = {
        "api_key": THINGSPEAK_WRITE_KEY,
        "field1": round(lat, 6),
        "field2": round(lng, 6),
        "field3": round(speed, 2),
        "field4": state_code
    }
    try:
        response = requests.post(url, data=payload, timeout=5)
        return response.text if response.status_code == 200 else False
    except Exception:
        return False

def generate_pdf_report():
    try:
        from fpdf import FPDF
    except ImportError:
        return
    pdf_filename = os.path.join(OS_REPORT_DIR, "route_incident_report.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(190, 10, "IoT Vehicle Tracking & Incident Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(40, 7, "Timestamp", 1, 0, "C")
    pdf.cell(30, 7, "Latitude", 1, 0, "C")
    pdf.cell(30, 7, "Longitude", 1, 0, "C")
    pdf.cell(25, 7, "Speed (km/h)", 1, 0, "C")
    pdf.cell(35, 7, "Status", 1, 0, "C")
    pdf.cell(30, 7, "Alert", 1, 1, "C")
    pdf.set_font("Helvetica", "", 8)
    if os.path.exists(CSV_DATA_PATH):
        with open(CSV_DATA_PATH, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in list(reader)[-20:]:
                pdf.cell(40, 6, row[0], 1, 0, "C")
                pdf.cell(30, 6, row[1], 1, 0, "C")
                pdf.cell(30, 6, row[2], 1, 0, "C")
                pdf.cell(25, 6, row[3], 1, 0, "C")
                pdf.cell(35, 6, row[4], 1, 0, "C")
                pdf.cell(30, 6, row[5], 1, 1, "C")
    pdf.output(pdf_filename)
    print(f"[+] PDF Report generated at: {pdf_filename}")

def main():
    print("=" * 70)
    print("      LAUNCHING COLD START LONG-DISTANCE TRACKING LOOP          ")
    print("=" * 70)
    
    # Large coordinate shifts to force the map background and labels to change noticeably
    simulation_steps = [
        {"scenario": "Starting Point", "lat_shift": 0.0000, "lng_shift": 0.0000, "speed": 0.0},
        {"scenario": "City Driving 1", "lat_shift": 0.0150, "lng_shift": 0.0150, "speed": 45.0},
        {"scenario": "City Driving 2", "lat_shift": 0.0320, "lng_shift": 0.0320, "speed": 55.0},
        {"scenario": "Highway Sprint", "lat_shift": 0.0680, "lng_shift": 0.0680, "speed": 92.0},
        {"scenario": "Border Breach",  "lat_shift": 0.1350, "lng_shift": 0.1350, "speed": 115.0}
    ]

    for step in simulation_steps:
        print(f"\n>>> Active Phase: [{step['scenario'].upper()}]")
        
        # Calculate new shifted coordinates stretching outward
        lat = HOME_LAT + step["lat_shift"]
        lng = HOME_LNG + step["lng_shift"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        computed_dist = calculate_haversine_distance(lat, lng, HOME_LAT, HOME_LNG)
        
        if computed_dist > GEOFENCE_RADIUS_METERS:
            status, alert_type, state_code = "BREACH_ALERT", "GEOFENCE_VIOLATION", 3
            print(f" [ALERT] Vehicle has traveled {computed_dist:.1f}m away from safety zone!")
        else:
            status, alert_type, state_code = "SAFE_ZONE", "NONE", 1
            
        print(f"    [{timestamp}] Lat: {lat:.6f} | Lng: {lng:.6f} | Dist: {computed_dist:.1f}m")
        print("    Syncing fresh coordinate cluster to Cloud View...")
        
        log_telemetry_to_csv(timestamp, lat, lng, step["speed"], status, alert_type)
        push_telemetry_to_cloud(lat, lng, step["speed"], state_code)
        
        # 15 second delay required by ThingSpeak free server limits
        time.sleep(15) 

    generate_pdf_report()
    print("=" * 70)

if __name__ == "__main__":
    main()