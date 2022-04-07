# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 6 (Sktime): ARIMA Automation ----

# Imports

import pandas as pd
import numpy as np

from my_pandas_extensions.database import collect_data
from my_pandas_extensions.timeseries import summarize_by_time

from sktime.forecasting.arima import AutoARIMA
from tqdm import tqdm


# WORKFLOW
df = collect_data()

bike_sales_m_df = df\
    .summarize_by_time(
    date_column = "order_date",
    value_column = "total_price",
    rule = "M",
    agg_func = np.sum,
    kind = "period",
    wide_format = True
)

bike_sales_cat2_m_df= df\
    .summarize_by_time(
    date_column = "order_date",
    value_column = "total_price",
    groups = "category_2",
    rule = "M",
    agg_func = np.sum,
    kind = "period",
    wide_format = True,
)

# Sktime Imports

# FUNCTION DEVELOPMENT ----
# - arima_forecast(): Generates ARIMA forecasts for one or more time series.

# """ 
#                                       WHAT WE ARE MAKING 
#                     arima_forecast()
#     A single Function that combines the for loop modeling iteration into a parameterized function.
    
    
#                                   PARAMETERIZING THE FUNCTION
#             Your function's arguments are going to be how we automate processing the forecast.
            
#             Choose these by reviewing the code for the task we are automating. 
            
#             Note: We can always come back later and add more parameters as our function evolves. 
# """


def arima_forecast(data, h,sp,alpha = 0.05, supress_warnings = True, *args, **kwargs):    

    # Checks 
    if (h is not int):
        raise Exception("`h` must be an integer")
    
    # Handle Inputs ---
    df = data
    
    # For Loop ----
    model_results_dict = {}
    for col in tqdm(df.columns, mininterval=0):
        # Series Extraction
        y = df[col]
        
    
    # Modeling
        forecaster = AutoARIMA(
            sp = sp,
            suppress_warnings= supress_warnings,
            *args,
            **kwargs
        )
        
        forecaster.fit(y)
        print(forecaster)
    
    # Prediction and Confidence Intervals 
        predictions, conf_int_df = forecaster.predict(
            fh               = np.arange(1,h+1),
            return_pred_int  = True,
            alpha= alpha
        )
        
    # Combine into data frame
        ret = pd.concat([y, predictions, conf_int_df], axis = 1)
        ret.columns = ["value", "predictions", "ci_low", "ci_high"]
        
        
    # Update Dictionary
        model_results_dict[col] = ret
        
    # Stacking each Dict on Top of each other
    
    
    model_results_df = pd.concat(model_results_dict, axis = 0)
    
    # Handle Column & Index Names
    
    nms = [*df.columns.names, *df.index.names]
    model_results_df.index.names = nms
    
    # Reset Index
    ret = model_results_df.reset_index()

    # Drop column containing str "level"
    cols_to_keep = ~ret.columns.str.startswith("level_")
    ret = ret.iloc[:,cols_to_keep]
            
    return ret
    

# Testing Function



arima_forecast(bike_sales_m_df, h = 12, sp = 1)
arima_forecast(bike_sales_cat2_m_df, h = 12, sp = 1)



# Import Test

from my_pandas_extensions.forecasting import arima_forecast

bike_sales_cat2_m_df \
    .arima_forecast(
        h = 12, 
        sp = 1
    )
    
# Plotting

# """ 
# Pandas grouped plots

# We can make multiple pandas plots using groupby()
# """

import matplotlib.pyplot as plt

forecast_df = bike_sales_cat2_m_df \
    .arima_forecast(
        h = 12, 
        sp = 1
    )
forecast_df\
    .groupby("category_2" ) \
            .plot(x = "order_date")
plt.show()