import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


def load_dataset(file_path):
    """
    Load the historical flight dataset.

    Args:
        file_path (str): Path to the CSV dataset.

    Returns:
        pandas.DataFrame
    """
    df = pd.read_csv(file_path)
    return pd.read_csv("../data/historical/flight_delays.csv")


def create_features(df):
    """
    Create new features used by the machine learning model.

    - DepartureHour
    - Month
    - DayOfWeek
    - Delayed (target)

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """

    df = df.copy()

    df["ScheduledDeparture"] = pd.to_datetime(df["ScheduledDeparture"])

    df["DepartureHour"] = df["ScheduledDeparture"].dt.hour
    df["Month"] = df["ScheduledDeparture"].dt.month
    df["DayOfWeek"] = df["ScheduledDeparture"].dt.dayofweek

    df["Delayed"] = (df["DelayMinutes"] >= 15).astype(int)

    return df


def select_features(df):
    """
    Keep only the columns required for machine learning.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """

    selected_columns = [
        "Airline",
        "Origin",
        "Destination",
        "DepartureHour",
        "Month",
        "DayOfWeek",
        "Distance",
        "AircraftType",
        "Delayed"
    ]

    return df[selected_columns].copy()


def encode_features(df):
    """
    Encode categorical columns using LabelEncoder.

    Args:
        df (pandas.DataFrame)

    Returns:
        tuple:
            df,
            airline_encoder,
            origin_encoder,
            destination_encoder,
            aircraft_encoder
    """

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
    """
    Split the dataset into training and testing sets.

    Args:
        df (pandas.DataFrame)

    Returns:
        X_train, X_test, y_train, y_test
    """

    X = df.drop("Delayed", axis=1)
    y = df["Delayed"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    return X_train, X_test, y_train, y_test
