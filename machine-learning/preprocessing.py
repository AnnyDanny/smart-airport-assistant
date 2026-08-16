import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def load_dataset(file_path):
    pd.read_csv(file_path)
    return pd.read_csv("../data/historical/flight_delays.csv")


def create_features(df):
    df = df.copy()
    df["ScheduledDeparture"] = pd.to_datetime(df["ScheduledDeparture"])
    df["DepartureHour"] = df["ScheduledDeparture"].dt.hour
    df["Month"] = df["ScheduledDeparture"].dt.month
    df["DayOfWeek"] = df["ScheduledDeparture"].dt.dayofweek
    df["Delayed"] = (df["DelayMinutes"] >= 15).astype(int)
    return df


def select_features(df):
    selected_columns = [
        "Airline",
        "Origin",
        "Destination",
        "DepartureHour",
        "Month",
        "DayOfWeek",
        "Distance",
        "AircraftType",
        "Delayed",
    ]
    return df[selected_columns].copy()


def encode_features(df):
    df = df.copy()

    airline_encoder = LabelEncoder()
    origin_encoder = LabelEncoder()
    destination_encoder = LabelEncoder()
    aircraft_encoder = LabelEncoder()

    df["Airline"] = airline_encoder.fit_transform(df["Airline"])
    df["Origin"] = origin_encoder.fit_transform(df["Origin"])
    df["Destination"] = destination_encoder.fit_transform(df["Destination"])
    df["AircraftType"] = aircraft_encoder.fit_transform(df["AircraftType"])

    return (
        df,
        airline_encoder,
        origin_encoder,
        destination_encoder,
        aircraft_encoder,
    )


def split_data(df):
    X = df.drop("Delayed", axis=1)
    y = df["Delayed"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )
    return X_train, X_test, y_train, y_test
