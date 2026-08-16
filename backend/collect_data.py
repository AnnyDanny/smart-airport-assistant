import json
from pathlib import Path

import pandas as pd
import requests

from backend.config import API_KEY

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "raw" / "flights_raw.json"
LIVE_FILE = BASE_DIR / "data" / "live" / "flights.csv"


def download_flights():
    url = "https://api.aviationstack.com/v1/flights"
    params = {
        "access_key": API_KEY,
        "dep_iata": "CPH",
    }
    response = requests.get(
        url,
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    if "data" not in data:
        raise ValueError("No flight data returned from AviationStack API.")
    return data


def save_raw_json(data):
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
            "FlightStatus": flight.get("flight_status"),
        }
        flights.append(flight_info)
    return flights


def save_csv(flights):
    LIVE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    df = pd.DataFrame(flights)
    df.to_csv(
        LIVE_FILE,
        index=False,
    )


def rebuild_csv_from_raw():
    if not RAW_FILE.exists():
        raise FileNotFoundError("flights_raw.json not found.")
    with open(RAW_FILE, "r") as file:
        data = json.load(file)
    flights = extract_flights(data)
    save_csv(flights)
    return len(flights)


def refresh_live_data():
    try:
        print("Downloading latest flights...")
        data = download_flights()
        save_raw_json(data)
        flights = extract_flights(data)
        save_csv(flights)
        print("Saved latest flights.csv")
    except requests.RequestException as e:
        print("Could not refresh live flights:", e)
        if RAW_FILE.exists():
            count = rebuild_csv_from_raw()
            print(f"Using cached data ({count} flights).")
        else:
            raise


def main():
    rebuild_csv_from_raw()


if __name__ == "__main__":
    main()
