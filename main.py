from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from predict import predict_energy

app = FastAPI(
    title="EcoDrive Core API",
    description="Energy prediction and risk assessment for EV delivery fleets.",
    version="0.2.0"
)


class TripInput(BaseModel):
    distance_km: float = Field(..., gt=0, description="Trip distance in kilometres")
    battery_pct: float = Field(..., ge=0, le=100, description="Current battery percentage")
    load_kg: float = Field(..., ge=0, description="Cargo load in kilograms")
    traffic_level: str = Field(..., description="Traffic level: 'low', 'medium', or 'high'")
    battery_capacity_kwh: Optional[float] = Field(40.0, gt=0, description="Battery capacity in kWh (default 40)")
    temperature_c: Optional[float] = Field(20.0, description="Ambient temperature in Celsius (default 20)")
    regen_efficiency: Optional[float] = Field(0.1, ge=0, le=1, description="Regenerative braking efficiency 0–1 (default 0.1)")
    vehicle_type: Optional[str] = Field("van", description="Vehicle type: 'car', 'van', or 'truck'")


@app.get("/")
def root():
    return {
        "system": "EcoDrive Core API",
        "version": "0.2.0",
        "status": "running",
        "endpoints": ["/predict-energy", "/health", "/docs"]
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict-energy")
def predict(trip: TripInput):
    try:
        result = predict_energy(
            distance_km=trip.distance_km,
            battery_pct=trip.battery_pct,
            load_kg=trip.load_kg,
            traffic_level=trip.traffic_level,
            battery_capacity_kwh=trip.battery_capacity_kwh,
            temperature_c=trip.temperature_c,
            regen_efficiency=trip.regen_efficiency,
            vehicle_type=trip.vehicle_type
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))