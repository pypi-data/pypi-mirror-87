# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 21:22:56 2020

@author: Dtime_PVF
"""

from datetime import datetime, timedelta
from seedftw.base.timeseries import split_data_loading_range

# Loading data from the API for 1 parameter
def split_api_calls(func, start, end, max_step, margin_last=timedelta(seconds=1)):
    """
    Function to split loading of data in a smart manner
    """

    # Create the steps for loading
    date_steps_range = split_data_loading_range(start=start, end=end, step=max_step)

    data = None
    for start_j, end_j in date_steps_range:
        data_j = func(start_j, end_j - margin_last)

        if data is None:
            data = data_j
        else:
            data = data.append(data_j)

    return data
