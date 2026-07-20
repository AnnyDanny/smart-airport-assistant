import joblib
import pandas as pd
from pathlib import Path
from datetime import timedelta
from backend.live_preprocessing import preprocess_live_flights

def safe_encode(value, encoder):
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    return 0

def load_model():
    BASE_DIR = Path(__file__).resolve().parent.parent
    models_dir = BASE_DIR / "models"
    model = joblib.load(models_dir / "model.pkl")

    airline_encoder = joblib.load(models_dir / "airline_encoder.pkl")
    origin_encoder = joblib.load(models_dir / "origin_encoder.pkl")
    destination_encoder = joblib.load(models_dir / "destination_encoder.pkl")
    aircraft_encoder = joblib.load(models_dir / "aircraft_encoder.pkl")
    return (
        model,
        airline_encoder,
        origin_encoder,
        destination_encoder,
        aircraft_encoder,
    )

def load_live_data():
    df = preprocess_live_flights()
    return df

def find_flight(df, flight_number):
    flight = df[
        df["FlightNumber"].str.upper() == flight_number.upper()
    ]
    if flight.empty:
        raise ValueError("Flight not found.")

    return flight.iloc[0]

def prepare_features(
    flight,
    airline_encoder,
    origin_encoder,
    destination_encoder,
    aircraft_encoder,
    ):
    features = {
        "Airline": safe_encode(
            flight["Airline"],
            airline_encoder
        ),
        "Origin": safe_encode(
            flight["Origin"],
            origin_encoder
        ),
        "Destination": safe_encode(
            flight["Destination"],
            destination_encoder
        ),
        "DepartureHour": flight["DepartureHour"],
        "Month": flight["Month"],
        "DayOfWeek": flight["DayOfWeek"],
        "Distance": 1000,
        "AircraftType": safe_encode(
            "Unknown",
            aircraft_encoder
        ),
    }
    return pd.DataFrame([features])

def predict_delay(model, features):
    probability = model.predict_proba(
        features
    )[0][1]
    return probability

def calculate_arrival_time(flight):
    departure = flight["ScheduledDeparture"]
    recommendation = departure - timedelta(hours=2)
    return recommendation

def calculate_congestion(df, flight):
    departure_hour = flight["DepartureHour"]
    nearby_flights = df[
        df["DepartureHour"].between(
            departure_hour - 1,
            departure_hour + 1
        )
    ]
    flights_count = len(nearby_flights)
    if flights_count < 10:
        return {
            "level": "Low",
            "percentage": 30
        }
    elif flights_count < 25:
        return {
            "level": "Moderate",
            "percentage": 60
        }
    else:
        return {
            "level": "High",
            "percentage": 85
        }

def build_recommendation(
    flight,
    probability,
    recommendation_time
    ):
    return {
        "FlightNumber": flight["FlightNumber"],
        "Airline": flight["Airline"],

        "Origin": flight["Origin"],
        "OriginAirport": flight["OriginAirport"],
        "ScheduledDeparture": str(flight["ScheduledDeparture"]),

        "Destination": flight["Destination"],
        "DestinationAirport": flight["DestinationAirport"],
        "ScheduledArrival": str(flight["ScheduledArrival"]),

        "Terminal": flight["Terminal"],
        "Gate": flight["Gate"],
        "FlightStatus": flight["FlightStatus"],
        "DelayProbability": round(probability, 2),
        "RecommendedArrival": recommendation_time.strftime("%d %b %Y, %H:%M"),
    }


def main():
    print("Loading model...")
    (
        model,
        airline_encoder,
        origin_encoder,
        destination_encoder,
        aircraft_encoder,
    ) = load_model()

    print("✓ Model loaded")

    print("\nLoading live flights...")
    df = load_live_data()
    print("✓ Live flights loaded")
    while True:
        print("\nAvailable flights:\n")
        print(
            df[
                [
                    "FlightNumber",
                    "Airline",
                    "Destination",
                    "FlightStatus",
                ]
            ].head(20)
        )
        flight_number = input(
            "\nEnter flight number: "
        ).strip()
        try:
            flight = find_flight(df, flight_number)
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
            recommendation_time = calculate_arrival_time(
                flight
            )
            recommendation = build_recommendation(
                flight,
                probability,
                recommendation_time,
            )
            print("\nRecommendation:")
            print(recommendation)
        except ValueError as error:
            print(f"\n{error}")
        answer = input(
            "\nSearch another flight? (y/n): "
        ).strip().lower()
        if answer != "y":
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
