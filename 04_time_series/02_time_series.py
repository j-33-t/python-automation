# DS4B 101-P: PYTHON FOR BUSINESS ANALYSIS ----
# Module 4 (Time Series): Working with Time Series Data ----

# IMPORTS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.resample import resample
from pandas.tseries import frequencies

from my_pandas_extensions.database import collect_data

# DATA

df = collect_data()

# 1.0 DATE BASICS

df['order_date']

# Conversion

"2011-01-07"

type("2011-01-07")

pd.to_datetime("2011-01-07")

pd.to_datetime("2011-01-07") \
    .to_period(freq="W") \
    .to_timestamp()

# Accessing elements

df.order_date

# Months

df.order_date.dt.month

df.order_date.dt.month_name()

# Days

df.order_date.dt.day
df.order_date.dt.day_name()

# Year

df.order_date.dt.year

# DATE MATH

import datetime

today = datetime.date.today()

today + pd.Timedelta(" 1 day") #shiting date by 1 day

pd.to_datetime(today + pd.Timedelta(" 1 day"))

df.order_date + pd.Timedelta("1Y") # shiting date by 1 year in dataframe

df.order_date + pd.Timedelta("30 min") 


# DURATION

today = datetime.date.today()

one_year_from_today = today + pd.Timedelta("1Y")

(one_year_from_today - today) / pd.Timedelta("1W")

""" 
Pandas TimeDelta objects are an "enhanced" version of datetime.timedelta objects.

They allow us to do more extended conversion like using "1M".

Use the approach below for months
"""

pd.Timedelta(one_year_from_today - today) / np.timedelta64(1, "M")



# DATE SEQUENCES

pd.date_range(
    start   = pd.to_datetime("2011"),
    periods = 5, 
    )

pd.date_range(
    start   = pd.to_datetime("2011-01"),
    periods = 30, 
    )

pd.date_range(
    start   = pd.to_datetime("2011-01"),
    periods = 365, 
    )

pd.date_range(
    start   = pd.to_datetime("2011"),
    periods = 5,
    freq= "2D" 
    )

pd.date_range(
    start   = pd.to_datetime("2011"),
    periods = 5,
    freq= "1W" 
    )

pd.date_range(
    start   = pd.to_datetime("2011"),
    periods = 5,
    freq= "1M" 
    )

pd.date_range(
    start   = pd.to_datetime("2011-01"),
    periods = 5,
    freq= "1Y" 
    )

# PERIODS
# - Periods represent timestamps that fall within an interval using a frequency.
# - IMPORTANT: {sktime} requires periods to model univariate time series
""" 
Sktime Pandas Support

According to Sktime Documenation , they support pandas integer, period and
timestamp indicies.

However, for plotting purposes, it is always preferable to use a time-based index.

There can be issues with forecasting using timestamp.
Period is the way to go for forecasting.


Periods are Never Ambiguous, TimeStamps are sometime Ambiguos

Periods have a defined frequency so extending them is not problem.
TimeStamps in Month and Yearly frequencies can be ambiguous because what is the duration 
of a month (28 days, 30 days?)

"""

# Convert to Time Stamp (converting datetime64 to period)

df.order_date
print(df.order_date.dtype)

df.order_date.dt.to_period(freq = "D")
print(df.order_date.dt.to_period(freq = "D").dtype)

""" 
Period : Coverts a timestamp point to an interval that contains that timestamp.

The intervals have fixed duration that can be modelded with a "frequency".

"""
df.order_date.dt.to_period(freq = "W")

""" 
Relationship to Resampling

When we resample, we are essentially collapsing data a Period by a frequency (rule).
Then using that frequency (rule) to period to perfrm operations

eg = np.sum() by "M" for month   
"""

df.order_date.dt.to_period(freq = "D")

df.order_date.dt.to_period(freq = "W")

df.order_date.dt.to_period(freq = "M")

df.order_date.dt.to_period(freq = "Q")

df.order_date.dt.to_period(freq = "Y")

# Get the Frequency

df.order_date.dt.to_period(freq = "D").dt.freq
df.order_date.dt.to_period(freq = "W").dt.freq

# Conversion to Timestamp

""" 
PRO TIP ! REMEMBER THESE.

pd.to_datetime() : Converts text to TimeStamp.

pd.to_period() : Converts TimeStamp to Period. 

pd.to_timestamp() : Converts Period to TimeStamp.

"""

df.order_date.dt.to_period(freq = "M").dt.to_timestamp() #changes to datetime64

df.order_date.dt.to_period(freq = "Q").dt.to_timestamp()


# TIME-BASED GROUPING (RESAMPLING)
# - The beginning of our Summarize by Time Function

# Single Time Series. Using kind = "timestamp"

bike_sales_m_df = df[['order_date', 'total_price']] \
    .set_index("order_date") \
        .resample("M", kind = "timestamp") \
            .sum() 

# Grouped Time Series Using kind = "period"

""" 
Order of operations for grouped resampling

1. Set Date column to Index (required for resampling )
2. Perform Grouping
3. Perform Resampling
3. Perform Aggregation
5. Reset Index
6. Period Conversion

"""

bike_sales_cat2_m_w_df = df[['category_2', 'order_date', 'total_price']] \
     .set_index("order_date") \
         .groupby("category_2") \
             .resample("M", kind = 'period') \
                 .agg(np.sum) \
                     .unstack("category_2") \
                     .reset_index() \
                         .assign(order_date = lambda x : x.order_date.dt.to_period("M")) \
                             .set_index("order_date")
                     

# MEASURING CHANGE

# Difference from Previous Timestamp

#  - Single (No Groups)

""" 
df.shit() : Creates a lag (or lead ) by shifting a series up or down.

Use positive values to create lags.
Use negative values to create leads.

Previous values (in our case total value) in new column is called a "lag" in Time Series Analysis.
"""

bike_sales_m_df \
    .assign(total_price_lag_1 = lambda x: x['total_price'].shift(1)) \
        .assign(difference = lambda x : x.total_price - x.total_price_lag_1) \
            .plot(y = 'difference')

plt.show()

# Same output as above but using apply function

bike_sales_m_df \
    .apply(lambda x : (x - x.shift(1))) \
        .plot()
plt.show()

"""Percentage Difference"""
bike_sales_m_df \
    .apply(lambda x : (x - x.shift(1) ) / x.shift(1) ) \
        .plot()
plt.show()



#  - Multiple Groups: Key is to use wide format with apply


bike_sales_cat2_m_w_df \
    .apply(lambda x : (x - x.shift(1) ) ) \
        .plot()
plt.show()


""" Percentage Difference """


bike_sales_cat2_m_w_df \
    .apply(lambda x : (x - x.shift(1) ) / (x.shift(1)) ) \
        .plot()

plt.show()
    

#  - Difference from First Timestamp

bike_sales_m_df \
    .apply( lambda x : (x - x[0]) )
    
bike_sales_m_df \
    .apply( lambda x : (x - x[0]) / x[0] )
    
bike_sales_m_df \
    .apply( lambda x : (x - x[0]) / x[0] ) \
        .plot()
plt.show()


# CUMULATIVE CALCULATIONS - single time series

bike_sales_m_df \
    .resample("YS") \
    .sum()
    
bike_sales_m_df \
    .resample("YS") \
    .sum() \
        .cumsum()
        
bike_sales_m_df \
    .resample("YS") \
    .sum() \
        .cumsum() \
            .reset_index() \
                .assign(order_date = lambda x: x.order_date.dt.to_period()) \
                    .set_index("order_date") \
            .plot(kind = "bar")  
plt.show()


# CUMULATIVE CALCULATIONS - multiple time series

bike_sales_cat2_m_w_df \
    .resample("Y") \
        .sum() \
            .cumsum() \
                .plot(kind = "bar", stacked = True)
plt.show()

# ROLLING CALCULATIONS

""" 
Moving Average : Probably the most common rolling calculation is the rolling mean (i.e Moving Average).

The Moving Average is where we specify a window length (eg 3 months) and we average every
data point using the 3 months preceding. 

It's used to smooth seasonality, identify trends, and even predict future values using an average
of the past.

It's also used very heavily in industries like Finance to develop stock technical indicators. 
"""

# Single

bike_sales_m_df.plot()
plt.show()

bike_sales_m_df['total_price'] \
    .rolling(
        window = 12
    ) \
        .mean()

bike_sales_m_df \
    .assign( total_price_roll12 = lambda x: x
            ["total_price"]\
                .rolling(
                    window = 12
                ) \
                    .mean()
                ) \
                    .plot()
plt.show()

"""
Right Alignment : The default is to right align, but this isn't always the best choice

We can "center" align with center = True

"""

bike_sales_m_df \
    .assign( total_price_roll12 = lambda x: x
            ["total_price"]\
                .rolling(
                    window = 12, 
                    center = True
                ) \
                    .mean()
                ) \
                    .plot()
plt.show()

""" 
min periods = "#"

Allows us to use "partial windows", which is when the full 12 windows aren't available 
we still return an average of as many observations as possible.

The effect is that it fills in the ends of the rolling calculation series. 

"""

bike_sales_m_df \
    .assign( total_price_roll12 = lambda x: x
            ["total_price"]\
                .rolling(
                    window = 12, 
                    center = True,
                    min_periods = 1
                ) \
                    .mean()
                )

bike_sales_m_df \
    .assign( total_price_roll12 = lambda x: x
            ["total_price"]\
                .rolling(
                    window = 12, 
                    center = True,
                    min_periods = 1
                ) \
                    .mean()
                ) \
                    .plot()
plt.show()


"""
Trend : Is the series going up or down over time ? [long term trend]

    - Large rolling averages show trend.  
    
"""

bike_sales_m_df \
    .assign( total_price_roll12 = lambda x: x
            ["total_price"]\
                .rolling(
                    window = 24, 
                    center = True,
                    min_periods = 1
                ) \
                    .mean()
                ) \
                    .plot()
plt.show()

"""

Smoothing: Is the series cycling ? (Seasonality)   [short term trend cyclical nature ]

    - Smaller rolling averages smooth the series.
"""

bike_sales_m_df \
    .assign( total_price_roll12 = lambda x: x
            ["total_price"]\
                .rolling(
                    window = 3, 
                    center = True,
                    min_periods = 1
                ) \
                    .mean()
                ) \
                    .plot()
plt.show()


# Groups - Can't use assign(), we'll use merging 

# Moving average multiple time series

multiple_time_series = bike_sales_cat2_m_w_df \
    .rolling(
        window = 24,
        center = True, 
        min_periods = 1
    ) \
        .mean() \
            .rename(lambda x: x + "_roll_24", axis = 1) \
                .merge(
                    bike_sales_cat2_m_w_df,
                    how =  "right",
                    left_index = True, 
                    right_index = True
                    )
                
multiple_time_series.plot()
plt.show()




# Accessing particular columns from a multi index dataframe for plotting side by side

a = multiple_time_series.iloc[:, multiple_time_series.columns.get_level_values("category_2") == 'Cross Country Race_roll_24']
b = multiple_time_series.iloc[:, multiple_time_series.columns.get_level_values("category_2") == 'Cross Country Race']

c = a.merge(b, on="order_date", how = "left")

c.plot()
plt.show()

