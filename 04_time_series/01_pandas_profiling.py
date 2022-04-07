# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 4 (Time Series): Profiling Data ----


# IMPORTS

import pandas as pd

from pandas_profiling import (ProfileReport, profile_report)

from my_pandas_extensions.database import collect_data

df = collect_data()

df

# PANDAS PROFILING

# Get a Profile
""" 
Python Classes : You may notice that this function is in CamelCase.

This is because ProfileReport is actually a Python Class, which are 
written in CapWords [aka CamelCase] per the python style-guide called
PEP 8. 

Other examples in Pandas are:
DataFrame()
Series()

This will become import when we begin extengin pandas.

ProfileReport(): It generates an HTML Profile Report that highlights 
                 key aspects of your data.
                 
"""

profile = ProfileReport(
    df = df
)

profile

# Sampling - Big Datasets

df.profile_report()

df.sample(frac = 0.5).profile_report()

# Pandas Helper
# ?pd.DataFrame.profile_report


# Saving Output

df.profile_report().to_file("04_time_series/profile_report.html")

# VSCode Extension - Browser Preview





