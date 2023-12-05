import requests
import pandas as pd
import numpy as np
import datetime as dt
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.preprocessing import StandardScaler
from geopy.distance import geodesic


class FetchDatetimeColumns(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.blizzard_dates = [
            dt.datetime(2016, 1, 23).date(),
            dt.datetime(2016, 1, 24).date(),
        ]
        self.hourly_bin_edges = [-1, 3, 6, 9, 12, 15, 18, 21, 24]
        self.hourly_buckets = [
            "0-3",
            "3-6",
            "6-9",
            "9-12",
            "12-15",
            "15-18",
            "18-21",
            "21-24",
        ]
        print("Datetime column formatting initialized")

    def fit(self, X):
        return self

    def transform(self, X):
        X_copy = (
            X.copy()
        )  # Create a copy of the DataFrame to avoid modifying the original
        X_copy["pickup_datetime"] = pd.to_datetime(X_copy["pickup_datetime"])
        X_copy["pickup_dayofweek"] = X_copy["pickup_datetime"].dt.dayofweek
        X_copy["pickup_date"] = X_copy["pickup_datetime"].dt.date
        X_copy["pickup_hour"] = X_copy["pickup_datetime"].dt.hour
        X_copy["pickup_timeofday"] = pd.cut(
            X_copy["pickup_hour"],
            bins=self.hourly_bin_edges,
            labels=self.hourly_buckets,
            right=False,
        )
        X_copy = X_copy.loc[~X_copy["pickup_date"].isin(self.blizzard_dates)]
        X_copy.drop(
            ["pickup_datetime", "pickup_date", "pickup_hour", "dropoff_datetime"],
            axis=1,
            inplace=True,
        )
        return X_copy


class FetchCategoricalColumns(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.passenger_bin_edges = [-1, 0, 3, 6, 9]
        self.passenger_buckets = ["0", "1-3", "4-6", "7-9"]
        print("Categorical column formatting initialized")

    def fit(self, X):
        return self

    def transform(self, X):
        X_copy = (
            X.copy()
        )  # Create a copy of the DataFrame to avoid modifying the original
        X_copy["passenger_count_bucket"] = pd.cut(
            X_copy["passenger_count"],
            bins=self.passenger_bin_edges,
            labels=self.passenger_buckets,
        )
        X_copy.drop(["passenger_count"], axis=1, inplace=True)
        columns_to_encode = [
            "vendor_id",
            "store_and_fwd_flag",
            "pickup_dayofweek",
            "pickup_timeofday",
            "passenger_count_bucket",
        ]
        ohe_X = pd.get_dummies(X_copy, columns=columns_to_encode, dtype=int)
        return ohe_X


class FetchDistances(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.precalculated_osrm_distances_df = pd.read_csv(
            "data/train_osrm_distances.csv"
        )
        print("Distance Calculation initialized")

    @staticmethod
    def osrm_distance(lat1, lon1, lat2, lon2, max_retries=3):
        url = f"http://127.0.0.1:5000/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
        retries = Retry(
            total=max_retries, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        for attempt in range(max_retries + 1):
            try:
                response = session.get(url)
                response.raise_for_status()

                if response.status_code == 200:
                    distance = response.json()["routes"][0]["distance"] / 1000
                    return distance
                else:
                    print(f"Error: {response.status_code}")
                    return np.nan

            except requests.exceptions.RequestException as e:
                print(f"Request failed on attempt {attempt + 1}/{max_retries + 1}: {e}")

        print(f"Maximum number of retries reached. Unable to complete the request.")
        return np.nan

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        coords_1 = (lat1, lon1)
        coords_2 = (lat2, lon2)
        return geodesic(coords_1, coords_2).kilometers

    def calculate_osrm_distance(self, lat1, lon1, lat2, lon2, dist):
        if np.isnan(dist):
            distance = self.osrm_distance(lat1, lon1, lat2, lon2)
            if np.isnan(distance):
                distance = self.haversine_distance(lat1, lon1, lat2, lon2)
            return distance
        else:
            return dist

    def fit(self, X):
        return self

    def transform(self, X):
        X_copy = X.copy()
        X_copy = pd.merge(
            X_copy,
            self.precalculated_osrm_distances_df[["id", "distance_osrm"]],
            on="id",
            how="left",
        )
        X_copy["distance_osrm"] = X_copy.apply(
            lambda row: self.calculate_osrm_distance(
                row["pickup_latitude"],
                row["pickup_longitude"],
                row["dropoff_latitude"],
                row["dropoff_longitude"],
                row["distance_osrm"],
            ),
            axis=1,
        )
        X_copy.drop(
            [
                "id",
                "pickup_longitude",
                "pickup_latitude",
                "dropoff_longitude",
                "dropoff_latitude",
            ],
            axis=1,
            inplace=True,
        )
        return X_copy


class ScaleDistances(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.standard_scaler = StandardScaler()
        print("Distance Scaling initialized")

    def fit(self, X):
        distance_data = X["distance_osrm"].values.reshape(-1, 1)
        self.standard_scaler.fit(distance_data)
        return self

    def transform(self, X):
        X_copy = X.copy()
        distance_data = X_copy["distance_osrm"].values.reshape(-1, 1)
        X_copy["scaled_distance_osrm"] = self.standard_scaler.transform(distance_data)
        X_copy.drop("distance_osrm", axis=1, inplace=True)
        X_final = X_copy.drop("trip_duration", axis=1)
        y_final = X_copy["trip_duration"]
        return X_final, y_final
