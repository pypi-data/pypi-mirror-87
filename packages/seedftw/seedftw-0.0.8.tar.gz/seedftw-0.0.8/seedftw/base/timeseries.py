# -*- coding: utf-8 -*-
"""
Functions related to timeseries management.

This file can also be imported as a module and contains the following
functions:

    * format_to_timetable - converts wind speed to power output of a wind turbine
    * synchronise - convert solar irradiance to the power output of a PV installation
    * resample_timeseries - resamples a timeseries to a given resolution
    * split_in_daily_profiles - splits a timeseries in a set of daily profiles
    * timestep_start - determines a timestep start for a given resolution
    * datetime_to_microepoch - converts a datetime to microepoch
    * microepoch_to_datetime_index - converts microepoch to datetime
    * microepoch_to_local_datetime - converts microepoch to a local datetime
    
"""

# Import all useful libraries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.tz import tzlocal
from pytz import timezone

# Helpers
def __is_timezone(var):
    class_name = str(var.__class__)
    return class_name.startswith("<class 'pytz.tzfile.") or class_name.startswith(
        "<class 'dateutil.tz.tz."
    )


def __get_local_timezone():
    return tzlocal()


# Dealing with timeseries data
def format_to_timetable(data, time_column="t", column_dict=None):
    """Formats a pandas dataframe into a timetable

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe to convert to timetable
    time_column : str
        Name of the column to use as time index
        (default: "t")
    column_dict : dict
        Dictionary to use for column renaming, if needed
        (default: None)

    Raises
    ------
    None

    Returns
    -------
    data : pd.DataFrame
        DataFrame indexed by time (timetable)
    """

    if len(data) == 0:
        return data

    if column_dict is not None:
        data = data.rename(columns=column_dict)

    if time_column != "t":
        data = data.rename(columns={time_column: "t"})

    if isinstance(data["t"][0], str):
        data["t"] = pd.to_datetime(data["t"])

    data = data.set_index("t").sort_index(ascending=True)
    return data


def synchronise(df1, df2, base="first", fill=None):
    """Formats a pandas dataframe into a timetable

    Parameters
    ----------
    df1 : pd.DataFrame
        First DataFrame to merge
    df2 : pd.DataFrame
        First DataFrame to merge
    base : str
        Time base for the merged DataFrame
        (options: "first","second","intersection","union")
        (default: "first")
    fill : str
        Filling method, if relevant
        (options: "backfill")
        (default: None)

    Raises
    ------
    None

    Returns
    -------
    data : pd.DataFrame
        DataFrame indexed by time (timetable)
    """

    # Some more hints here: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#resampling

    if base == "first":
        df_m = df1.merge(df2, how="left", right_index=True, left_index=True)

    elif base == "second":
        df_m = df1.merge(df2, how="right", right_index=True, left_index=True)

    elif base == "intersection":
        df_m = df1.merge(df2, how="intersection", right_index=True, left_index=True)

    elif base == "union":
        df_m = df1.merge(df2, how="outer", right_index=True, left_index=True)

    else:
        raise Exception("This case is not supported : " + base)

    if fill is not None:
        if fill == "backfill":
            df_m = df_m.fillna("backfill", axis="index")
        else:
            raise Exception("This fill is not supported yet: " + base)

    return df_m


def resample_timeseries(data, resolution="raw", function="mean"):
    """Resamples a timeseries at a given frequency

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame to resample
    resolution : str
        Resolution to use for the daily profile
        (options: "raw","hour","day")
        (default: "raw")
    function : str
        Function to use for the resampling
        (options: "mean","min","max","sum")
        (default: "mean")

    Raises
    ------
    None

    Returns
    -------
    T_split : pd.DataFrame
        DataFrame of containing the split of the daily profiles, indexed by date
    """

    if resolution == "raw" or data is None or len(data) == 0:
        None

    else:
        if resolution == "hour":
            resampler = data.resample("H")
        elif resolution == "day":
            resampler = data.resample("D")
        else:
            raise Exception("Illegal value of data resolution: " + resolution)

        if function == "mean":
            data = resampler.mean()
        elif function == "sum":
            data = resampler.sum()
        elif function == "min":
            data = resampler.min()
        elif function == "max":
            data = resampler.max()
        else:
            raise Exception("Illegal value of function: " + function)

    return data


def split_in_daily_profiles(data, column, resolution="hour", time_zone="UTC"):
    """Formats a pandas dataframe into a timetable

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame to split in daily profiles
    column : str
        Name of the column to split in daily profiles
    resolution : str
        Resolution to use for the daily profile
        (options: "hour","15min","10min","5min")
        (default: "hour")
    time_zone : str or pytz timezone
        Time-zone for the daily profile
        (default: "UTC")

    Raises
    ------
    None

    Returns
    -------
    T_split : pd.DataFrame
        DataFrame of containing the split of the daily profiles, indexed by date
    """
    data_copy = data[[column]].copy()
    data_copy["date"] = data_copy.index.date

    if isinstance(time_zone, str):
        target_tz = timezone(time_zone)
    elif __is_timezone(time_zone):
        target_tz = time_zone
    else:
        raise Exception(
            "Invalid format for input 'time_zone' (must be either str or pytz timezone)"
        )

    data_copy.index = data_copy.index.tz_convert(target_tz)

    T_split = (
        pd.DataFrame({"date": data_copy.index.date})
        .drop_duplicates(subset=["date"])
        .set_index("date")
    )

    if resolution == "hour":
        data_copy["timeOfDay"] = data_copy.index.hour
        range2use = range(0, 24, 1)
        col_name = lambda x: "H" + str(x)

    elif resolution == "15min":
        data_copy["timeOfDay"] = data_copy.index.hour * 60 + data_copy.index.minute
        range2use = range(0, 24 * 60, 15)
        col_name = lambda x: "M15_" + str(int(x / 15))

    elif resolution == "10min":
        data_copy["timeOfDay"] = data_copy.index.hour * 60 + data_copy.index.minute
        range2use = range(0, 24 * 60, 10)
        col_name = lambda x: "M10_" + str(int(x / 10))

    elif resolution == "5min":
        data_copy["timeOfDay"] = data_copy.index.hour * 60 + data_copy.index.minute
        range2use = range(0, 24 * 60, 5)
        col_name = lambda x: "M5_" + str(int(x / 5))

    else:
        raise Exception("Illegal resolution: " + resolution)

    for i in range2use:
        T_i = (
            data_copy[[column, "date"]]
            .loc[data_copy["timeOfDay"] == i]
            .set_index("date")
        )
        T_i = T_i.rename(columns={column: col_name(i)})
        T_split = T_split.merge(T_i, how="left", right_index=True, left_index=True)

    return T_split


def split_data_loading_range(start_date, end_date, step=timedelta(weeks=24)):
    date_range = []
    max_date = lambda x: np.min([end_date, x + step])
    time_1 = start_date
    time_2 = start_date
    while time_2 < end_date:
        time_1 = time_2
        time_2 = max_date(time_1)
        date_range.append([time_1, time_2])

    return date_range


def timestep_start(step, t=None):

    if t is None:
        t = datetime.now(__get_local_timezone())

    if step == "second" or step == "1s":
        t_start = t.replace(microsecond=0)
    elif step == "15s":
        sec_start = int(t.second / 15) * 15
        t_start = t.replace(microsecond=0, second=sec_start)
    elif step == "30s":
        sec_start = int(t.second / 30) * 30
        t_start = t.replace(microsecond=0, second=sec_start)
    elif step == "minute" or step == "1min":
        t_start = t.replace(microsecond=0, second=0)
    elif step == "5min":
        min_start = int(t.minute / 5) * 5
        t_start = t.replace(microsecond=0, second=0, minute=min_start)
    elif step == "15min":
        min_start = int(t.minute / 15) * 15
        t_start = t.replace(microsecond=0, second=0, minute=min_start)
    elif step == "30min":
        min_start = int(t.minute / 30) * 30
        t_start = t.replace(microsecond=0, second=0, minute=min_start)
    elif step == "hour":
        t_start = t.replace(microsecond=0, second=0, minute=0)
    elif step == "day":
        t_start = t.replace(microsecond=0, second=0, minute=0, hour=0)
    elif step == "month":
        t_start = t.replace(microsecond=0, second=0, minute=0, hour=0, day=1)
    elif step == "year":
        t_start = t.replace(microsecond=0, second=0, minute=0, hour=0, day=1, month=1)
    else:
        raise Exception("Unknown setp: " + step)

    return t_start


# Functions dealing with microepoch data
def datetime_to_microepoch(datetimes2use):
    return int(datetimes2use.timestamp() * 1e6)


def microepoch_to_datetime_index(microepoch):
    t = pd.DatetimeIndex(np.round(microepoch).astype("datetime64[us]"))
    return t.tz_localize("UTC")


def microepoch_to_local_datetime(microepoch):
    t = pd.Datetime(np.round(microepoch).astype("datetime64[us]"))
    return t.tz_localize(__get_local_timezone())
