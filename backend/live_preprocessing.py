import pandas as pd
from backend.collect_data import refresh_live_data
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LIVE_FILE = BASE_DIR / "data" / "live" / "flights.csv"


def load_live_flights():
    return pd.read_csv(LIVE_FILE)

def create_time_features(df):
    required_columns = [
        "ScheduledDeparture",
        "ScheduledArrival",
    ]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")
    df["ScheduledDeparture"] = pd.to_datetime(
        df["ScheduledDeparture"],
        utc=True
    )
    df["ScheduledArrival"] = pd.to_datetime(
        df["ScheduledArrival"],
        utc=True
    )
    df["DepartureHour"] = df["ScheduledDeparture"].dt.hour
    df["Month"] = df["ScheduledDeparture"].dt.month
    df["DayOfWeek"] = df["ScheduledDeparture"].dt.dayofweek
    return df

def fill_missing_values(df):
    df["Terminal"] = (
        df["Terminal"]
        .fillna("Unknown")
        .astype(str)
        .str.replace(".0", "", regex=False)
    )
    df["Gate"] = df["Gate"].fillna("Unknown")
    df["DepartureDelay"] = df["DepartureDelay"].fillna(0)
    df["ArrivalDelay"] = df["ArrivalDelay"].fillna(0)
    return df

def select_columns(df):
    columns = [
        "FlightNumber",
        "Airline",
        "Origin",
        "OriginAirport",
        "Destination",
        "DestinationAirport",
        "ScheduledDeparture",
        "ScheduledArrival",
        "DepartureHour",
        "Month",
        "DayOfWeek",
        "Terminal",
        "Gate",
        "DepartureDelay",
        "ArrivalDelay",
        "FlightStatus",
    ]
    return df[columns]

def preprocess_live_flights():
    refresh_live_data()
    df = load_live_flights()
    df = create_time_features(df)
    df = fill_missing_values(df)
    df = select_columns(df)
    return df
