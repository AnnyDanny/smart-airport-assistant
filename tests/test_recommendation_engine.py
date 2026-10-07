from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest

from backend.recommendation_engine import (
    build_recommendation,
    calculate_arrival_time,
    calculate_congestion,
    find_flight,
    predict_delay,
    prepare_features,
    safe_encode,
)


class MockEncoder:
    def __init__(self):
        self.classes_ = ["SAS", "KLM"]

    def transform(self, values):
        mapping = {"SAS": 0, "KLM": 1}
        return [mapping[value] for value in values]


class MockModel:
    def predict_proba(self, features):
        return [[0.75, 0.25]]


def test_safe_encode_known_value():
    encoder = MockEncoder()

    result = safe_encode("SAS", encoder)

    assert result == 0


def test_safe_encode_unknown_value():
    encoder = MockEncoder()

    result = safe_encode("UNKNOWN", encoder)

    assert result == 0


def test_find_flight():
    df = pd.DataFrame(
        {
            "FlightNumber": ["SK123", "KL456"],
            "Airline": ["SAS", "KLM"],
        }
    )

    flight = find_flight(df, "sk123")

    assert flight["FlightNumber"] == "SK123"


def test_find_flight_not_found():
    df = pd.DataFrame(
        {
            "FlightNumber": ["SK123", "KL456"],
            "Airline": ["SAS", "KLM"],
        }
    )

    with pytest.raises(ValueError, match="Flight not found."):
        find_flight(df, "XX999")


def test_prepare_features():
    flight = pd.Series(
        {
            "Airline": "SAS",
            "Origin": "CPH",
            "Destination": "LHR",
            "DepartureHour": 14,
            "Month": 10,
            "DayOfWeek": 2,
        }
    )

    encoder = MockEncoder()

    features = prepare_features(
        flight,
        encoder,
        encoder,
        encoder,
        encoder,
    )

    assert len(features) == 1
    assert list(features.columns) == [
        "Airline",
        "Origin",
        "Destination",
        "DepartureHour",
        "Month",
        "DayOfWeek",
        "Distance",
        "AircraftType",
    ]
    assert features.iloc[0]["DepartureHour"] == 14
    assert features.iloc[0]["Month"] == 10
    assert features.iloc[0]["DayOfWeek"] == 2
    assert features.iloc[0]["Distance"] == 1000


def test_predict_delay():
    model = MockModel()

    features = pd.DataFrame(
        {
            "Airline": [0],
            "Origin": [0],
            "Destination": [1],
        }
    )

    probability = predict_delay(model, features)

    assert probability == 0.25


def test_calculate_arrival_time():
    departure = datetime(2026, 10, 7, 14, 30, tzinfo=timezone.utc)

    flight = pd.Series({"ScheduledDeparture": departure})

    result = calculate_arrival_time(flight)

    assert result == departure - timedelta(hours=2)


def test_calculate_congestion_low():
    df = pd.DataFrame({"DepartureHour": [14, 14, 15]})

    flight = pd.Series({"DepartureHour": 14})

    result = calculate_congestion(df, flight)

    assert result == {"level": "Low", "percentage": 30}


def test_calculate_congestion_moderate():
    df = pd.DataFrame({"DepartureHour": [14] * 15})

    flight = pd.Series({"DepartureHour": 14})

    result = calculate_congestion(df, flight)

    assert result == {"level": "Moderate", "percentage": 60}


def test_calculate_congestion_high():
    df = pd.DataFrame({"DepartureHour": [14] * 30})

    flight = pd.Series({"DepartureHour": 14})

    result = calculate_congestion(df, flight)

    assert result == {"level": "High", "percentage": 85}


def test_build_recommendation():
    departure = datetime(2026, 10, 7, 14, 30, tzinfo=timezone.utc)
    arrival = datetime(2026, 10, 7, 16, 20, tzinfo=timezone.utc)

    flight = pd.Series(
        {
            "FlightNumber": "SK123",
            "Airline": "SAS",
            "Origin": "CPH",
            "OriginAirport": "Copenhagen Airport",
            "ScheduledDeparture": departure,
            "Destination": "LHR",
            "DestinationAirport": "Heathrow Airport",
            "ScheduledArrival": arrival,
            "Terminal": "3",
            "Gate": "A12",
            "FlightStatus": "scheduled",
        }
    )

    result = build_recommendation(
        flight,
        0.25,
        departure - timedelta(hours=2),
    )

    assert result["FlightNumber"] == "SK123"
    assert result["Airline"] == "SAS"
    assert result["Origin"] == "CPH"
    assert result["Destination"] == "LHR"
    assert result["DelayProbability"] == 0.25
    assert result["Terminal"] == "3"
    assert result["Gate"] == "A12"
    assert result["FlightStatus"] == "scheduled"
    assert result["RecommendedArrival"] == "07 Oct 2026, 12:30"
