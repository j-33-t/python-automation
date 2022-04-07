# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 8 (SQL Database Update): Forecast Write and Read Functions ----

# IMPORTS ----

import sqlalchemy as sql
from sqlalchemy.types import (String, Numeric)
from sqlalchemy.sql.schema import MetaData

import pandas as pd
import numpy as np

from my_pandas_extensions.database import collect_data
from my_pandas_extensions.timeseries import summarize_by_time
from my_pandas_extensions.forecasting import (arima_forecast, plot_forecast)


# Data Import

df = collect_data()

# WORKFLOW ----
# - Until Module 07: Visualization

arima_forecast_df = df \
    .summarize_by_time(
        date_column  = "order_date",
        value_column = "total_price",
        groups       = "category_2",
        rule         = "M",
        agg_func     = np.sum,
        kind         = "period",
        wide_format  = True,
        fillna       = 0
    ) \
        .arima_forecast(
            h                = 12,
            sp               = 1,
            supress_warnigns = True,
            alpha            = 0.05
        )

arima_forecast_df.plot_forecast(
    id_column = "category_2",
    date_column = "order_date",
    facet_ncol = 3
)

###################################################################################################
##                                                                                               ##
##                                 -------- PRO TIP !! -----------                               ##
##                 Store Important Parts of Your Automation Workflow in a Database.              ##          
##                                                                                               ##
##         These are parts of your workflow that others need access to when you aren't around.   ##    
##                                                                                               ##
###################################################################################################

# DATABASE UPDATE FUNCTIONS ----




# 1.0 PREPARATION FUNCTIONS ---- [Standardize the data and prep for database]
##################################################################################################
##                                                                                              ##
##                                 -------- PRO TIP !! -----------                              ##
##                                  Standardizing Column Names.                                 ##      
##                      It is essential if the data is going into a database                    ##
##                                                                                              ##
##         In database-speak, this is part of a concept called schema, which is used to         ##
##         specify the way your database is set up and how it connects to other tables if       ##
##         relationship exists.                                                                 ##
##         This table won't have any connections , but it's still a good idea to standardize    ##
##         the naming                                                                           ##    
##                                                                                              ##
##################################################################################################

# Idea to implement
arima_forecast_df \
    .rename(
        {
        "category_2": "id",
        "order_date": "date"
    }, axis = 1
        )

data = arima_forecast_df
id_column = "category_2"
date_column = "order_date"

# Creating Function     
def prep_forecast_data_for_update(data, id_column, date_column):
    
    # Format column names to standardize
    df = data.rename(
        {
        id_column: "id",
        date_column: "date"
    }, axis = 1
        )
    
    # Validate correct columns
    
    required_column_names = ['id', 'date', 'value', 'predictions','ci_low', 'ci_high']
    
    if not all(pd.Series(required_column_names).isin(df.columns)):
        col_text = ", ".join(required_column_names)
        raise Exception(f"Columns must contain: {col_text}")
     
     
    return(df)

# Testing function 
prep_forecast_data_for_update(
    data = arima_forecast_df,
    id_column= "category_2",
    date_column= "order_date"
)

# Testing function with missing column -> "ci_low"

prep_forecast_data_for_update(
    data = arima_forecast_df.drop("ci_low", axis = 1),
    id_column= "category_2",
    date_column= "order_date"
)

# Testing function prep_forecast_data_for_update()
prep_forecast_data_for_update(arima_forecast_df, id_column="category_2", date_column="order_date")


# 2.0 WRITE TO DATABASE ---- [Send data to the Database]

def write_forecast_to_database(data, id_column, date_column, 
                               conn_string = "sqlite:///00_database/bike_orders_database.sqlite",
                               table_name = "forecast", if_exists = "fail",
                               **kwargs):
    
    # Prepare the data
    df = prep_forecast_data_for_update(
        data        = data,
        id_column   = id_column,
        date_column = date_column
    )
    
    # Check format for SQL Database
    
    ##########################################################################
    #               SQLite stores Dates as Strings.                          #
    #       SQLite: No Date/Date-Time Format. It stores as a string.         #
    #                                                                        #
    #       This means we need to format our dates so we can easily convert  # 
    #       to and from Pandas Timestamp.                                    #
    #                                                                        #
    ##########################################################################
    
    df['date'] = df['date'].dt.to_timestamp()
    
    #########################################################################
    #                                                                       #
    #                   SQLite Data Type Storage.                           #    
    #       SQLAlchemy includes a variety of dtype functions to specify     #   
    #       how to store each column of data                                #
    #                                                                       #
    #       This is useful for setting up the SQL table properly            #                               
    #                                                                       #      
    #########################################################################
    
    # 
    #                     PRO-TIP!!
    #         Specify your database data types. 
    #        
    #         This will help you avoid erros and make sure your data is stored
    #         in a format that you can work with.
    #                
    # 
    
    sql_dtypes = {
        "id"         :  String(),
        "date"       :  String(),
        "value"      :  Numeric(),
        "predictions":  Numeric(),
        "ci_low"     :  Numeric(),
        "ci_high"    :  Numeric
    }
    
    
    # Connect to Database
    
    engine = sql.create_engine(conn_string)
    
    conn = engine.connect()
    
    
    # Create table
    df.to_sql(
        con       = conn, 
        name      = table_name,
        if_exists = if_exists,
        dtype     = sql_dtypes,
        index = False
        # **kwargs
    )
    
    # Close Connection
    
    conn.close()
    
    pass


# Testing
write_forecast_to_database(
    data        = arima_forecast_df,
    id_column   = "category_2",
    date_column = "order_date",
    if_exists   = "replace"
)

# Testing 2 [creating a table and removing it]
# `Creating new table forecast_2`
write_forecast_to_database(
    data        = arima_forecast_df,
    id_column   = "category_2",
    date_column = "order_date",
    table_name= "forecast_2",
    if_exists   = "replace"
)

# `removing table`
conn_string = "sqlite:///00_database/bike_orders_database.sqlite"
engine = sql.create_engine(conn_string)
conn = engine.connect()
sql.Table("forecast_2",MetaData(conn)).drop()

# 3.0 READ FROM DATABASE ---- [Import data from the Database]

def read_forecast_from_database(conn_string = "sqlite:///00_database/bike_orders_database.sqlite",
                                table_name = "forecast",
                                **kwargs):
    
    # Connect to Database
    engine = sql.create_engine(conn_string)
    
    conn = engine.connect()
    
    # Read From Table
    df = pd.read_sql(f"SELECT * FROM {table_name}", con = conn, parse_dates= ['date'])
    
    # Close connection
    conn.close()
    
    return df

# Testing

read_forecast_from_database()