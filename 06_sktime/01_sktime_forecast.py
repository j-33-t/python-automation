# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 6 (Sktime): Introduction to Forecasting ----

# Imports

import pandas as pd
import numpy as np

from my_pandas_extensions.database import collect_data

from my_pandas_extensions.timeseries import summarize_by_time

import matplotlib.pyplot as plt

df = collect_data()

# Sktime Imports

from sktime.forecasting.arima import AutoARIMA
from sktime.utils.plotting import plot_series

# Progress Bars Import

from tqdm import tqdm  # Pro-Tip : use tqdm() in your long running scripts. 
                       #If something takes longer than 2 seconds without showing progress, people think it's an error


# 1.0 DATA SUMMARIZATIONS ----

# """ 
#           --- Data Aggregation is Critical to Forecasting ----

#   We can't have raw timestamp data. We need to have time series aggregated 
#   so that each point in time is unique to a time series group.

# """


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

# 2.0 SINGLE TIME SERIES FORECAST ----

# """ 
#                 FORECASTING
#         Taking the historical demand data and estimating (predicting) the next `h` observations into the future
        
#                 Regression 
#         Predicting Numeric Values. As compared to classfication, which is selecting classes by probabilities.
        
#         Time Series is a Sub-Field of Data Science
#     It is very Important to business analysis
    
# """

bike_sales_m_df.plot()
plt.show()


# ARIMA [AutoRegressive Integrated Moving Average]

# """
#     ---- STATIONARITY ----
#     The view that you need to deterend the series before you can accurately regress it.
#     This removes any upward or downward trend.
    
#     Detrending can be performed through a process called differencing. 
    
#     AutoARIMA incorporates differencing, so the incoming series does not need to be sationary. !!!
    
#     ---- DIFFERENCING ----
#     When a time series is subtracted (diff'ed) by it's lag1.
#                 diff = y(t) - y(t-1)
#     The effect is converting a series to differences, which removes any trend making the series stationary.
    
#     AutoARIMA takes care of this automatically !!!
    
#     AutoARIMA is made for busy people
#     AutoARIMA takes care of selecting most parameters.
    
#     It's a good candidate algorithm for iteration because of it's hands-off "auto" forecasting capability.
    
# """

# """ 
#                 FORECASTING WITH SKTIME
#         STEP 1: Make a forecaster
#         STEP 2: Fit the forecaster to data (usually a panda series)
#         STEP 3: Predict

#         Most Import Argument in AutoArima [sp = Seasonal Period]
        
#         If there are cycles in your data (e.g every 12 months is a cycle),
#         You need to tell AutoArima this

#         Since we have a monthly dataset, we have a cycle after 12 months, therefore for us sp = 12
        
        
#             TO MANY WARNINNGS , Whats Happening ?
#         The AutoARIMA algorithm is working. 
#         It's cycling thorugh different parameters.
        
#         Some of the parameters won't work, but this is normal.
        
#         What's important is that it finds parameters that do work.
        
#                     PREDICT
#         The predict() method tells the trained forecaster to estimate future values
#         in the time series sequence
#         fh in predict() means forecast horizon
        
# # """

# """ 
#     SciKit Learn Machine Learning Library
    
#     These are the same steps you'll use with Scikit Learn machine learning library
    
#     Step 1: Make a model spec
#     Step 2: Fit the model spec to data
#     Step 3: Predict using the fitted model
# """

bike_sales_m_df

y = bike_sales_m_df["total_price"]

forecaster = AutoARIMA(sp = 24)

forecaster.fit(y)

# --------------- PREDICTIONS ---------------

h = 12
forecaster.predict(fh = np.arange(1,h+1))


# """ 
#                 Confidence Intervals
#         These measure how confident we are in the estimate
        
#         Note that these are "Prediction Intervals" based on in-sample estimates.
        
#         These are not out-of-sample(gold standard) for confidence / accuracy measurement.
        
#         Sktime has methods to do out-of-sample, which requires a second round of training to get
#         accuracy metrics like (RMSE, MAE, etc)
# """


# --------------- CONFIDENCE INTERVALS ---------------

# saving using tuple unpacking because predict is return complex tuple object 
predictions_series, conf_int_df = forecaster.predict(
    fh = np.arange(1, h+1),
    return_pred_int= True,
    alpha = 0.05 # This will give us an 80%  prediction interval
    )


predictions_series

conf_int_df

# --------------- VISUALIZE ---------------
# Forecasting visualization (is absolutely critical, never shortcut this step)



plot_series(
    y,
    predictions_series,
    conf_int_df["lower"],
    conf_int_df["upper"],
    labels = ["actual", "prediction", "ci_lower", "ci_upper"]
)
plt.show()

# 3.0 MULTIPLE TIME SERIES FORCAST (LOOP) ----


# """
#             Scaling UP
#     We're going to tackle modeling multiple time series 
#     using a for loop

# """

# """ 
#             Hierarchical Forecast
#     Drilling into sales by Product Category is an example of a 
#     Hierarchy where total sales is comprised of many products.
    
#     Companies often want to "Drill in" and segment the revenue by revenue
#     stream (eg. product category, customer, region, etc)
# """



df = bike_sales_cat2_m_df

df.columns

df.columns[0]
df.columns[1]

df[df.columns[1]]

# PRO TIP: use print() statements when debugging your code.
# This helps to see what intermediate output is being generated and can highlight issues.

model_results_dict = {}
for col in tqdm(df.columns):
    
    # Series Extraction
    
    y = df[col]
    
    # Modeling 
    
    forecaster = AutoARIMA(
        sp = 12,
        suppress_warnings= True
    )
    
    forecaster.fit(y)
    
    # Predictions and Confidence Intervals
    
    h = 12
    predictions, conf_int_df = forecaster.predict(
        fh               = np.arange(1,h+1),
        return_pred_int  = True,
        alpha= 0.05
    )
    
    # Combine Into a DataFrame
    ret = pd.concat([y, predictions, conf_int_df], axis = 1)
    # PRO-TIP: Standardizing the column names of the output is a good idea. 
    #          It makes it much easier to program when the names that are output are consistent.
    #          We'll standardize as: "value", "prediction", "ci_low", "ci_high"
    ret.columns = ["value", "predictions", "ci_low", "ci_high"]
    
    # Update dictionary
    model_results_dict[col] = ret
    
model_results_dict


model_results_dict.keys()

model_results_dict[("total_price","Cross Country Race")]
# Pro-Tip : Append data structure indicators to your variable names. 
# This helps big time with remembering what format variables are stored.

model_results_df = pd.concat(model_results_dict, axis = 0)



# PRO-Tip : Always visualize your work (especially when forecasting). 
# You will quite often locate erros and issues that need to be addressed in your code.

# VISUALIZE

model_results_dict[("total_price","Cross Country Race")].plot()
plt.show()

list(model_results_dict.keys())[1]
model_results_dict[list(model_results_dict.keys())[0]].plot()
plt.show()