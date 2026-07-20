from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.recommendation_engine import (
    load_model,
    load_live_data,
    find_flight,
    calculate_congestion,
    prepare_features,
    predict_delay,
    calculate_arrival_time,
    build_recommendation,
)
from backend.weather_service import get_weather

(
    model,
    airline_encoder,
    origin_encoder,
    destination_encoder,
    aircraft_encoder,
) = load_model()

app = FastAPI(
    title="Smart Airport Assistant API",
    description="Machine Learning API for flight delay prediction.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Smart Airport Assistant API is running."
    }

@app.get("/flights")
def get_flights():
    df = load_live_data()
    flights = df[
        [
            "FlightNumber",
            "Airline",
            "Destination",
            "FlightStatus",
        ]
    ]
    return flights.to_dict(
        orient="records"
    )

@app.get("/predict/{flight_number}")
def get_prediction(flight_number: str):
    df = load_live_data()
    try:
        flight = find_flight(
            df,
            flight_number
        )
        weather = get_weather()
        congestion = calculate_congestion(
            df,
            flight,
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Flight not found."
        )
    features = prepare_features(
        flight,
        airline_encoder,
        origin_encoder,
        destination_encoder,
        aircraft_encoder,
    )
    probability = predict_delay(
        model,
        features,
    )

    recommendation = calculate_arrival_time(
        flight
    )

    result = build_recommendation(
        flight,
        probability,
        recommendation,
    )
    result["Congestion"] = congestion
    result["Weather"] = weather
    return result
