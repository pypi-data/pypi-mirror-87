# -*- coding: utf-8 -*-
"""
Functions related to data loading in Great Britain.

Sources:
- https://carbonintensity.org.uk/

"""

import pandas as pd
import requests
from datetime import datetime, timedelta
from pytz import timezone, UTC
from dateutil.parser import parse

from seedftw.base.timeseries import (
    format_to_timetable,
    resample_timeseries,
    timestep_start,
)
from seedftw.base.tricks import split_api_calls

# For caching
from functools import lru_cache

__uk_timezone = "Europe/London"
__api_url = "https://api.carbonintensity.org.uk/"

# Loading data from CarbonIntensity.org.uk
@lru_cache(maxsize=10)
def __api_call(endpoint):
    r = requests.get(__api_url + endpoint)

    data = r.json()

    if "error" in data.keys():
        status = data["error"]["code"]
    else:
        status = 200

    if status == 200:
        None
    elif status.startswith("400"):
        raise Exception("Bad request (on endpoint: {})".format(endpoint))
    elif status.startswith("500"):
        raise Exception("Internal server error (on endpoint: {})".format(endpoint))
    else:
        raise Exception(
            "Unknown return status={} (on endpoint: {})".format(status, endpoint)
        )

    return data


def __convert_string_to_datetime(string):
    return parse(string)


def get_emission_factors(out="dict"):
    endpoint = "intensity/factors"
    r = __api_call(endpoint)
    data = r["data"][0]

    low_format = out.lower()

    if low_format == "dict":
        return data
    elif low_format == "dataframe":
        return pd.DataFrame(
            {"technology": data.keys(), "emission_intensity": data.values()}
        )
    else:
        raise Exception("Unknown format: " + out)


def __load_historical_intensity(start, end):
    endpoint = "intensity/{}/{}".format(start.isoformat(), end.isoformat())
    r = __api_call(endpoint)
    raw_data = pd.DataFrame(r["data"])
    raw_data["start"] = pd.to_datetime(raw_data["from"])
    raw_data[["forecast", "actual", "index"]] = raw_data["intensity"].apply(pd.Series)

    raw_data2 = pd.DataFrame(raw_data["intensity"])

    data = format_to_timetable(
        raw_data[["start", "forecast", "actual"]], time_column="start", column_dict=None
    )
    return data


def get_historical_intensity(
    start=timestep_start("30min") - timedelta(days=2),
    end=timestep_start("30min"),
    resolution="raw",
):
    max_step = timedelta(days=13)
    data = split_api_calls(
        __load_historical_intensity,
        start,
        end,
        max_step,
        margin_last=timedelta(seconds=1),
    )

    data = resample_timeseries(
        data, resolution=resolution, function="mean", timezone=__uk_timezone
    )
    return data
