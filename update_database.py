# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 9 (Jupyter Automated Reporting): Update Database ----

# IMPORTS ----

import pandas as pd
import numpy as np

from my_pandas_extensions.database import (
    collect_data,
    write_forecast_to_database,
    read_forecast_from_database,
    prep_forecast_data_for_update
)

from my_pandas_extensions.timeseries import summarize_by_time
from my_pandas_extensions.forecasting import arima_forecast, plot_forecast

df = collect_data()


# 1.0 SUMMARIZE AND FORECAST ----


# 1.1 Total Revenue ----

print("Forecast 1/4: Forecasting Total Revenue...\n")

forecast_1_df = df \
    .summarize_by_time(
        date_column  = "order_date",
        value_column = "total_price",
        rule         = "M",
        kind         = "period"
    ) \
    .arima_forecast(
        h  = 12, 
        sp = 12
    )

forecast_1_df = forecast_1_df \
    .assign(id = "Total Revenue") \
    .prep_forecast_data_for_update(
        id_column   = "id",
        date_column = "order_date"
    )

print("Forecast 1/4: Forecasting Total Revenue Complete\n")



# 1.2 Revenue by Category 1 ----

print("Forecast 2/4: Forecasting Category 1...\n")

forecast_2_df = df \
    .summarize_by_time(
        date_column   = "order_date",
        value_column  = "total_price",
        groups        = "category_1", 
        rule          = "M",
        kind          = "period"
    ) \
    .arima_forecast(
        h   = 12, 
        sp  = 12
    )

forecast_2_df = forecast_2_df \
    .prep_forecast_data_for_update(
        id_column    = "category_1",
        date_column  = "order_date"
    ) \
    .assign(id = lambda x: "Category 1: " + x['id']) 

print("Forecast 2/4: Forecasting Category 1 Complete\n")

# 1.3 Revenue by Category 2 ----

print("Forecast 3/4: Forecasting Category 2...\n")

forecast_3_df = df \
    .summarize_by_time(
        date_column   = "order_date",
        value_column  = "total_price",
        groups        = "category_2", 
        rule          = "M",
        kind          = "period"
    ) \
    .arima_forecast(
        h   = 12, 
        sp  = 12
    )

forecast_3_df = forecast_3_df \
    .prep_forecast_data_for_update(
        id_column   = "category_2",
        date_column = "order_date"
    ) \
    .assign(id = lambda x: "Category 2: " + x['id']) 

print("Forecast 3/4: Forecasting Category 3 Complete\n")

# 1.4 Revenue by Customer ----

print("Forecast 4/4: Forecasting Revenue by Customer...\n")

forecast_4_df = df \
    .summarize_by_time(
        date_column   = "order_date",
        value_column  = "total_price",
        groups        = "bikeshop_name", 
        rule          = "Q",
        kind          = "period"
    ) \
    .arima_forecast(
        h   = 4,
        sp  = 4
    ) 

forecast_4_df = forecast_4_df \
    .prep_forecast_data_for_update(
        id_column   = "bikeshop_name",
        date_column = "order_date"
    ) \
    .assign(id = lambda x: "Bikeshop: " + x['id']) 

print("Forecast 4/4: Forecasting Revenue by Customer Complete\n")

# 2.0 UPDATE DATABASE ----

print("Updating Database")

all_forecasts_df = pd.concat(
    [
        forecast_1_df, 
        forecast_2_df,
        forecast_3_df,
        forecast_4_df
    ], 
    axis = 0
)

all_forecasts_df

# 2.1 Write to Database ----

all_forecasts_df \
    .write_forecast_to_database(
        id_column   = "id",
        date_column = "date",
        if_exists   = "replace"
    )

print("Database update complete.")