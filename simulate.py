import requests

scenarios = [
    {"distance_km": 20, "battery_pct": 80, "load_kg": 50, "traffic_level": "low"},
    {"distance_km": 60, "battery_pct": 30, "load_kg": 200, "traffic_level": "high"},
    {"distance_km": 35, "battery_pct": 50, "load_kg": 150, "traffic_level": "medium"},
    {"distance_km": 10, "battery_pct": 90, "load_kg": 30, "traffic_level": "low"},
    {"distance_km": 80, "battery_pct": 20, "load_kg": 250, "traffic_level": "high"},
    {"distance_km": 25, "battery_pct": 65, "load_kg": 100, "traffic_level": "medium"},
    {"distance_km": 55, "battery_pct": 45, "load_kg": 180, "traffic_level": "high"},
    {"distance_km": 15, "battery_pct": 75, "load_kg": 60, "traffic_level": "low"},
    {"distance_km": 70, "battery_pct": 25, "load_kg": 220, "traffic_level": "high"},
    {"distance_km": 40, "battery_pct": 55, "load_kg": 130, "traffic_level": "medium"},
]

print("EcoDrive Core — Delivery Simulation\n")
for i, s in enumerate(scenarios):
    r = requests.post("http://127.0.0.1:8000/predict-energy", json=s)
    result = r.json()
    print(f"Scenario {i+1}: {s['distance_km']}km | {s['battery_pct']}% battery | {s['load_kg']}kg | {s['traffic_level']} traffic")
    print(f"  → {result['estimated_kwh']} kWh | Risk: {result['risk']} | {result['suggestion']}\n")