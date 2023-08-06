# -*- coding: utf-8 -*-
"""
Functions related to data loading in Denmark.

API specification is found on:
    https://confluence.govcloud.dk/pages/viewpage.action?pageId=15303111

functions:

    * get_weather_stations - loads the list of all Danish weather stations
    * get_weather_station_data - loads historical data for a given station
    * get_closest_weather_station - identifies the closest weather station
    * get_data_for_coordinates - loads historical data from the closest station
        to a set of coordinates

"""

# Import all useful libraries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

from seedftw.exceptions import MissingApiKeyError
from seedftw.environment.geography import distance_between_coordinates
from seedftw.base.tricks import split_api_calls
from seedftw.base.timeseries import resample_timeseries

# For caching
from functools import lru_cache

__dk_timezone = "Europe/Copenhagen"


def _get_api_key():
    api_key_field = "SEEDFTW:API_KEY:DK:DMI"
    dmi_api_key = os.getenv(api_key_field)
    if dmi_api_key is None:
        e = MissingApiKeyError(
            message="Missing API key for DMI service.",
            environment_variable=api_key_field,
            create_at_url="https://confluence.govcloud.dk/display/FDAPI",
        )
        raise e

    return dmi_api_key


# Functions dealing with microepoch data
from seedftw.base.timeseries import (
    format_to_timetable,
    datetime_to_microepoch,
    microepoch_to_datetime_index,
    microepoch_to_local_datetime,
    synchronise,
    split_data_loading_range,
)


def _datetime_to_microepoch(datetimes2use):
    return datetime_to_microepoch(datetimes2use)


def _microepoch_to_datetime_index(microepoch):
    return microepoch_to_datetime_index(microepoch)


def _microepoch_to_local_datetime(microepoch):
    return microepoch_to_local_datetime(microepoch)


def __format_data_table(data):
    return format_to_timetable(data, time_column="Minutes5UTC", column_dict=None)


# Loading data from DMI's API
@lru_cache(maxsize=10)
def __dmi_api_call(address):

    api_key_part = "api-key=" + _get_api_key()

    query_url = "https://dmigw.govcloud.dk/" + address
    if "?" in query_url:
        binding_sym = "&"
    else:
        binding_sym = "?"

    ur_2_call = query_url + binding_sym + api_key_part

    # Read data in Json format
    result = pd.read_json(ur_2_call)

    return result


# Loading data from the API for 1 parameter
def __sub_load_parameter_timeseries(station, parameter, start, end, resolution):
    """
    Documentation of the details of the data is available here:
    >>  https://confluence.govcloud.dk/pages/viewpage.action?pageId=26476616
    """

    if isinstance(station, str):
        station_string = station
    else:
        station_string = str(station).zfill(5)

    parameter2id = {
        "ambient_temperature": "temp_dry",
        "wind_speed": "wind_speed",
        "wind_direction": "wind_dir",
        "relative_humidity": "humidity",
        "global_solar_radiation": "radia_glob",
    }

    # Adding a query size limiter to approx. 6 months
    limit2use = 30000

    start_microepoch = _datetime_to_microepoch(start)
    end_microepoch = _datetime_to_microepoch(end)
    query_url = "metObs/v1/observation?from={}&to={}&stationId={}&parameterId={}&limit={}".format(
        str(start_microepoch),
        str(end_microepoch),
        station_string,
        parameter2id[parameter],
        str(limit2use),
    )

    dmi_raw_data = __dmi_api_call(query_url)
    dmi_raw_data["t"] = _microepoch_to_datetime_index(dmi_raw_data["timeObserved"])
    data = format_to_timetable(
        dmi_raw_data[["t", "value"]],
        time_column="t",
        column_dict={"value": parameter},
    )
    return data


def __load_parameter_timeseries(station, parameter, start, end, resolution):

    # Split calls
    max_step = timedelta(weeks=24)
    margin_last = timedelta(seconds=1)
    func = lambda t0, t1: __sub_load_parameter_timeseries(
        station, parameter, t0, t1, resolution
    )
    data = split_api_calls(func, start, end, max_step, margin_last)

    # Resample
    data = resample_timeseries(
        data, resolution=resolution, function="mean", timezone=__dk_timezone
    )

    return data


@lru_cache(maxsize=1)
def get_weather_stations():
    """Loads the list of the Danish weather stations

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    stations : pandas.DataFrame(height,latitude,longitude,name,type,stationId)
        Details of the weather stations
    """
    T = __dmi_api_call("metObs/v1/station?country=DNK")

    stations = T["location"].apply(pd.Series)
    stations["name"] = T["name"]
    stations["type"] = T["type"]
    stations["stationId"] = T["stationId"]

    return stations


def get_weather_station_data(
    station=6031,
    start=(datetime.now() - timedelta(days=3)),
    end=datetime.now(),
    resolution="hour",
    parameters=["ambient_temperature"],
):
    """Loads historical data for a given weather station

    Parameters
    ----------
    station : int or str
        stationId of the station for which data is to be loaded
    start : datetime
        Time for the start of the historical period
    end: datetime
        Time for the end of the historical period
    resolution: str
        Resolution of the data to load (raw,hour,day)
    parameters : list(str)
        List of parameters to be loaded
        (Options: "ambient_temperature","wind_speed","wind_direction",
         "relative_humidity","global_solar_radiation")

    Raises
    ------
    None

    Returns
    -------
    data : pandas.DataFrame(t,ambient_temperature)
        Timetable of the ambient temperature [degrees C]


    Documentation of the details of the data is available here:
    >>  https://confluence.govcloud.dk/pages/viewpage.action?pageId=26476616

    """

    if isinstance(station, str):
        station_string = station
    else:
        station_string = str(station).zfill(5)

    data = None

    for par_i in parameters:
        data_i = __load_parameter_timeseries(station, par_i, start, end, resolution)
        if data is None:
            data = data_i
        else:
            data = synchronise(data, data_i, "union")

    return data


def get_closest_weather_station(latitude, longitude):
    """Identifies the closest weather station for a set geographical coordinates

    Parameters
    ----------
    latitude : float
        Latitude [degrees]
    longitude : float
        Longitude [degrees]

    Raises
    ------
    None

    Returns
    -------
    closest_station : pandas.Series(height,latitude,longitude,name,type,stationId)
        Details of the closest location
    """

    # Get all DMI locations
    dmi_stations = get_weather_stations()

    # Selecting the ones with all weather data available
    selected_stations = dmi_stations.loc[dmi_stations["type"] == "Synop", :]

    distance_to_stations = selected_stations.apply(
        lambda row: distance_between_coordinates(
            [latitude, longitude], [row["latitude"], row["longitude"]]
        ),
        axis=1,
    )

    closest_index = selected_stations.index[np.argmin(distance_to_stations)]
    closest_station = selected_stations.loc[closest_index, :]

    return closest_station


def get_data_for_coordinates(
    latitude=57.046707,
    longitude=9.935932,
    start=(datetime.now() - timedelta(days=3)),
    end=datetime.now(),
    resolution="hour",
    parameters=["ambient_temperature"],
):
    """Loads historical data from the closest weather station to a set of coordinates

    Parameters
    ----------
    latitude : float
        Latitude [degrees]
    longitude : float
        Longitude [degrees]
    start : datetime
        Time for the start of the historical period
    end: datetime
        Time for the end of the historical period
    resolution: str
        Resolution of the data to load (raw,hour,day)
    parameters : list(str)
        List of parameters to be loaded
        (Options: "ambient_temperature","wind_speed","wind_direction",
         "relative_humidity","global_solar_radiation")

    Raises
    ------
    None

    Returns
    -------
    data : pandas.DataFrame(t,ambient_temperature)
        Timetable of the ambient temperature [degrees C]
    """

    closest_station = get_closest_weather_station(latitude, longitude)
    data = get_weather_station_data(
        station=closest_station["stationId"],
        start=start,
        end=end,
        resolution=resolution,
        parameters=parameters,
    )
    return data
