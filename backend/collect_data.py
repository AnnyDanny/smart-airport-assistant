
from pathlib import Path
import requests
from backend.config import API_KEY
import json
import pandas as pd


def download_flights():
    url = "https://api.aviationstack.com/v1/flights"
    params = {
    "access_key": API_KEY,
    "dep_iata": "CPH"
    }
    response = requests.get(url, params=params)
    data = response.json()
    response.raise_for_status()
    for flight in data["data"]:
        if "data" not in data:
            raise ValueError("No flight data returned from AviationStack API.")
    return data

def save_raw_json(data):
    BASE_DIR = Path(__file__).resolve().parent.parent
    raw_dir = BASE_DIR / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    with open(raw_dir / "flights_raw.json", "w") as file:
        json.dump(data, file, indent=4)

def extract_flights(data):
    flights = []
    for flight in data["data"]:
        flight_info = {
            "FlightNumber": flight.get("flight", {}).get("iata"),
            "Airline": flight.get("airline", {}).get("name"),

            "Origin": flight.get("departure", {}).get("iata"),
            "OriginAirport": flight.get("departure", {}).get("airport"),

            "Destination": flight.get("arrival", {}).get("iata"),
            "DestinationAirport": flight.get("arrival", {}).get("airport"),

            "ScheduledDeparture": flight.get("departure", {}).get("scheduled"),
            "ScheduledArrival": flight.get("arrival", {}).get("scheduled"),

            "Terminal": flight.get("departure", {}).get("terminal"),
            "Gate": flight.get("departure", {}).get("gate"),

            "DepartureDelay": flight.get("departure", {}).get("delay"),
            "ArrivalDelay": flight.get("arrival", {}).get("delay"),

            "FlightStatus": flight.get("flight_status")
        }
        flights.append(flight_info)
    return flights

def save_csv(flights):
    df = pd.DataFrame(flights)
    BASE_DIR = Path(__file__).resolve().parent.parent
    live_dir = BASE_DIR / "data" / "live"
    live_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(live_dir / "flights.csv", index=False)

def refresh_live_data():
    data = download_flights()
    save_raw_json(data)

    flights = extract_flights(data)
    save_csv(flights)

def main():
    data = download_flights()
    save_raw_json(data)
    flights = extract_flights(data)
    save_csv(flights)
    print(f"Downloaded {len(flights)} flights.")
    print("Saved raw JSON to data/raw/flights_raw.json")
    print("Saved CSV to data/live/flights.csv")
    df = pd.read_csv("data/live/flights.csv")
    print(df.columns)

if __name__ == "__main__":
    main()
