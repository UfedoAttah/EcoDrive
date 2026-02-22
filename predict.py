def predict_energy(
    distance_km: float,
    battery_pct: float,
    load_kg: float,
    traffic_level: str,
    battery_capacity_kwh: float = 40.0,
    temperature_c: float = 20.0,
    regen_efficiency: float = 0.1,
    vehicle_type: str = "van"
) -> dict:
    """
    EcoDrive Core — Energy Prediction Engine v0.2

    Parameters:
        distance_km           : Trip distance in kilometres
        battery_pct           : Current battery percentage (0–100)
        load_kg               : Cargo load in kilograms
        traffic_level         : 'low', 'medium', or 'high'
        battery_capacity_kwh  : Vehicle battery capacity (default 40kWh)
        temperature_c         : Ambient temperature in Celsius (default 20°C)
        regen_efficiency      : Regenerative braking efficiency (0–1, default 0.1)
        vehicle_type          : 'van', 'car', or 'truck'

    Returns:
        dict with energy estimate, arrival battery %, risk score, and recommendation
    """

    # --- Input Validation ---
    if distance_km < 0:
        raise ValueError("distance_km cannot be negative.")
    if not (0 <= battery_pct <= 100):
        raise ValueError("battery_pct must be between 0 and 100.")
    if battery_capacity_kwh <= 0:
        raise ValueError("battery_capacity_kwh must be a positive number.")
    if load_kg < 0:
        raise ValueError("load_kg cannot be negative.")
    if not (0 <= regen_efficiency <= 1):
        raise ValueError("regen_efficiency must be between 0 and 1.")
    if traffic_level not in ["low", "medium", "high"]:
        raise ValueError(f"Invalid traffic_level '{traffic_level}'. Use 'low', 'medium', or 'high'.")
    if vehicle_type not in ["van", "car", "truck"]:
        raise ValueError(f"Invalid vehicle_type '{vehicle_type}'. Use 'van', 'car', or 'truck'.")

    # --- Base Consumption by Vehicle Type (kWh per km) ---
    base_rate = {
        "car": 0.15,
        "van": 0.20,
        "truck": 0.30
    }[vehicle_type]

    # --- Factors ---
    load_factor = 1 + (load_kg / 500)

    traffic_factor = {
        "low": 1.0,
        "medium": 1.15,
        "high": 1.35
    }[traffic_level]

    # Cold weather increases consumption; heat has minor effect
    if temperature_c < 20:
        temp_factor = 1 + ((20 - temperature_c) * 0.012)  # ~1.2% per degree below 20°C
    elif temperature_c > 35:
        temp_factor = 1 + ((temperature_c - 35) * 0.005)  # AC load above 35°C
    else:
        temp_factor = 1.0

    # Regenerative braking saves energy (more effective in stop-start / high traffic)
    regen_multiplier = {"low": 0.5, "medium": 1.0, "high": 1.5}[traffic_level]
    regen_savings = distance_km * 0.02 * regen_efficiency * regen_multiplier

    # --- Core Calculation ---
    gross_consumption = distance_km * base_rate * load_factor * traffic_factor * temp_factor
    estimated_kwh = max(0, gross_consumption - regen_savings)

    # --- Battery State ---
    energy_available = (battery_pct / 100) * battery_capacity_kwh
    energy_remaining = energy_available - estimated_kwh
    arrival_battery_kwh = max(0, energy_remaining)
    arrival_pct = round((arrival_battery_kwh / battery_capacity_kwh) * 100, 1)

    # --- Risk Score (0.0 = no risk, 1.0 = critical) ---
    if energy_available <= 0:
        risk_score = 1.0
    else:
        risk_score = round(1 - (energy_remaining / energy_available), 2)
        risk_score = max(0.0, min(1.0, risk_score))

    # --- Risk Classification ---
    if risk_score < 0.35:
        risk = "Low"
        suggestion = "Continue as planned."
    elif risk_score < 0.70:
        risk = "Medium"
        suggestion = "Optimize route to reduce energy usage."
    else:
        risk = "High"
        suggestion = "Charge before departure."

    # --- Trip Feasibility ---
    feasible = energy_remaining > 0

    return {
        "vehicle_type": vehicle_type,
        "distance_km": distance_km,
        "estimated_kwh": round(estimated_kwh, 2),
        "arrival_battery_pct": arrival_pct,
        "risk_score": risk_score,
        "risk": risk,
        "suggestion": suggestion,
        "trip_feasible": feasible,
        "inputs": {
            "battery_pct": battery_pct,
            "battery_capacity_kwh": battery_capacity_kwh,
            "load_kg": load_kg,
            "traffic_level": traffic_level,
            "temperature_c": temperature_c,
            "regen_efficiency": regen_efficiency
        }
    }


# --- Quick Test ---
if __name__ == "__main__":
    import json

    test_cases = [
        # Normal trip
        (45, 60, 120, "medium"),
        # Winter UK conditions
        (60, 50, 180, "high", 75, 3),
        # Light city run
        (15, 90, 30, "low", 40, 18, 0.2, "car"),
        # Heavy truck, low battery
        (80, 25, 400, "high", 100, 5, 0.05, "truck"),
    ]

    for t in test_cases:
        try:
            result = predict_energy(*t)
            print(json.dumps(result, indent=2))
            print("-" * 50)
        except ValueError as e:
            print(f"Validation error: {e}\n")

    # Edge case tests
    print("=== Edge Case Tests ===")
    edge_cases = [
        (-10, 60, 120, "medium"),
        (45, 105, 120, "medium"),
        (45, 60, 120, "hurricane"),
        (45, 60, -50, "low"),
    ]

    for t in edge_cases:
        try:
            predict_energy(*t)
        except ValueError as e:
            print(f"Caught: {e}")