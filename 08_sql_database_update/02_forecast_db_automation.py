# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 8 (SQL Database Update): Forecast Automation ----

# IMPORTS ----

import pandas as pd
import numpy as np

from my_pandas_extensions.database import  (collect_data, write_forecast_to_database, 
                                            read_forecast_from_database, prep_forecast_data_for_update,
                                            convert_to_datetime)
from my_pandas_extensions.timeseries import summarize_by_time
from my_pandas_extensions.forecasting import (arima_forecast, plot_forecast)
# Read Data

df = collect_data()

# 1.0 SUMMARIZE AND FORECAST ----


# 1.1 Total Revenue ----
forecast1_df = df \
    .summarize_by_time(
        date_column = "order_date",
        value_column = "total_price",
        rule = "M",
        kind = "period"
    ) \
        .arima_forecast(
            h = 12,
            sp = 12
        ) \
            .assign(id = "Total Revenue") #adding an extra column because we don't have groups otherwise plot will throw error
            
forecast1_df = forecast1_df \
    .prep_forecast_data_for_update(
        id_column = "id",
        date_column = "order_date"
    )
    
forecast1_df \
    .plot_forecast(
        id_column = "id",
        date_column = "date"
    )

# 1.2 Revenue by Category 1 ----
forecast2_df = df \
    .summarize_by_time(
        date_column  = "order_date",
        value_column = "total_price",
        groups       = "category_1",
        rule         = "M",
        kind         = "period"
    ) \
        .arima_forecast(
            h  = 12,
            sp = 12
        )

forecast2_df = forecast2_df \
    .prep_forecast_data_for_update(
        id_column = "category_1",
        date_column = "order_date"
    )

forecast2_df \
    .plot_forecast(
        id_column = "id",
        date_column = "date"
    )

# 2 forecast stacked
pd.concat([forecast1_df,forecast2_df], axis = 0) \
    .plot_forecast(
        id_column = "id",
        date_column = "date"
    )

# 1.3 Revenue by Category 2 ----
forecast3_df = df \
    .summarize_by_time(
        date_column  = "order_date",
        value_column = "total_price",
        groups       = "category_2",
        rule         = "M",
        kind         = "period"
    ) \
        .arima_forecast(
            h  = 12,
            sp = 12
        )
        
forecast3_df = forecast3_df \
    .prep_forecast_data_for_update(
        id_column = "category_2",
        date_column = "order_date"
    )

# 3 forecast stacked and faceted
pd.concat([forecast1_df,forecast2_df, forecast3_df], axis = 0) \
    .plot_forecast(
        id_column = "id",
        date_column = "date",
        facet_ncol = 3
    )


# 1.4 Revenue by Customer [Quaterly]----
forecast_qaterly_df = df \
    .summarize_by_time(
        date_column  = "order_date",
        value_column = "total_price",
        groups       = "bikeshop_name",
        rule         = "Q",
        kind         = "period"
    ) \
        .arima_forecast(
            h  = 4,
            sp = 4
        )

forecast_qaterly_df = forecast_qaterly_df \
    .prep_forecast_data_for_update(id_column = "bikeshop_name",date_column = "order_date")

# 4 forecast stacked and faceted    
pd.concat([forecast1_df,forecast2_df, forecast3_df,forecast_qaterly_df], axis = 0) \
    .plot_forecast(
            id_column = "id",
            date_column = "date",
            facet_ncol = 3
        )
    
# 2.0 UPDATE DATABASE ----
all_forecasts_df = pd.concat([forecast1_df,forecast2_df, forecast3_df,forecast_qaterly_df], axis = 0)

# PRO-TIP !! SAVE INTERMEDIATE DATA TO SAVE TIME when debugging

all_forecasts_df.to_pickle("./08_sql_database_update/allforecast_df.pkl")

all_forecasts_df = pd.read_pickle("./08_sql_database_update/allforecast_df.pkl")

# 2.1 Write to Database ----


all_forecasts_df \
    .write_forecast_to_database(
        id_column = "id",
        date_column = "date",
        if_exists = "replace"
    )

# 2.2 Read from Database ----
all_forecasts_form_db_df = read_forecast_from_database()

all_forecasts_form_db_df.info()