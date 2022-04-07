

# IMPORTS ----

import sqlalchemy as sql
from sqlalchemy.types import String, Numeric

import pandas as pd

import pandas_flavor as pf


# COLLECT DATA ----
def collect_data(conn_string = "sqlite:///00_database/bike_orders_database.sqlite"):  
    """
    Collects and combines the bike orders data. 

    Args:
        conn_string (str, optional): A SQLAlchemy connection string to find the database. Defaults to "sqlite:///00_database/bike_orders_database.sqlite".

    Returns:
        DataFrame: A pandas data frame that combines data from tables:
        
            - orderlines: Transactions data
            - bikes: Products data
            - bikeshops: Customers data
    """

    # Body

    # 1.0 Connect to database

    engine = sql.create_engine(conn_string)

    conn = engine.connect()

    table_names = ['bikes', 'bikeshops', 'orderlines']

    data_dict = {}
    for table in table_names:
        data_dict[table] = pd.read_sql(f"SELECT * FROM {table}", con=conn) \
            .drop("index", axis=1)
    
    conn.close()

    # 2.0 Combining Data

    joined_df = pd.DataFrame(data_dict['orderlines']) \
        .merge(
            right    = data_dict['bikes'],
            how      = 'left',
            left_on  = 'product.id',
            right_on = 'bike.id'
        ) \
        .merge(
            right    = data_dict['bikeshops'],
            how      = "left",
            left_on  = "customer.id",
            right_on = 'bikeshop.id'
        )

    # 3.0 Cleaning Data 

    df = joined_df

    df['order.date'] = pd.to_datetime(df['order.date'])

    temp_df = df['description'].str.split(" - ", expand = True)
    df['category.1'] = temp_df[0]
    df['category.2'] = temp_df[1]
    df['frame.material'] = temp_df[2]

    temp_df = df['location'].str.split(", ", expand = True)
    df['city'] = temp_df[0]
    df['state'] = temp_df[1]

    df['total.price'] = df['quantity'] * df['price']

    df.columns

    cols_to_keep_list = [
        'order.id', 'order.line', 'order.date',    
        'quantity', 'price', 'total.price', 
        'model', 'category.1', 'category.2', 'frame.material', 
        'bikeshop.name', 'city', 'state'
    ]

    df = df[cols_to_keep_list]

    df.columns = df.columns.str.replace(".", "_",regex=False)

    # df.info()

    return df


# PREP FORECAST -----
@pf.register_dataframe_method
def prep_forecast_data_for_update(
    data, id_column, date_column
    ):

    # Format the column names
    df = data \
        .rename(
            {
                id_column   : 'id',
                date_column : 'date'
            },
            axis = 1
        )

    # Validate correct columns
    required_col_names = [
        'id', 'date', 'value', 
        'predictions', 'ci_low', 'ci_high'
    ]

    if not all(pd.Series(required_col_names).isin(df.columns)):
        col_text = ", ".join(required_col_names)
        raise Exception(f"Columns must contain: {col_text}")  

    # Reorder columns
    df = df[required_col_names]

    # Check format for SQL Database
    # df['date'] = df['date'].dt.to_timestamp()
    df = convert_to_datetime(df, "date")

    return(df)

# WRITE FORECAST ----

@pf.register_dataframe_method
def write_forecast_to_database(
    data, id_column, date_column, 
    conn_string = "sqlite:///00_database/bike_orders_database.sqlite", 
    table_name = "forecast",
    if_exists = "fail",
    **kwargs
):
    """Writes the forecast table to the database

    Args:
        data (DataFrame): 
            An ARIMA forecast Data Frame.
        id_column (str): 
            A single column name specifying a unique identifier for the time series
        date_column (str): 
            A single column name specifying the date column.
        conn_string (str, optional): 
            A connection string to database to be updated. Defaults to "sqlite:///00_database/bike_orders_database.sqlite".
        table_name (str, optional): 
            Table name for the table to be created or modified. Defaults to "forecast".
        if_exists (str, optional): 
            Used to determine how the table is updated if the table exists. Passed to pandas.to_sql(). Defaults to "fail".
        **kwargs: 
            Additional arguments passed to pandas.to_sql().

    See also:
        - my_pandas_extensions.forecasting.arima_forecast()
    """

    # Prepare the data
    df = prep_forecast_data_for_update(
        data        = data, 
        id_column   = id_column,
        date_column = date_column
    )

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

    sql_dtype = {
        "id"         : String(),
        "date"       : String(),
        "value"      : Numeric(),
        "predictions" : Numeric(),
        "ci_low"      : Numeric(),
        "ci_high"      : Numeric()
    }

    # Connect to Database

    engine = sql.create_engine(conn_string)

    conn = engine.connect()

    # Make Table

    df.to_sql(
        con       = conn,
        name      = table_name,
        if_exists = if_exists,
        dtype     = sql_dtype,
        index     = False,
        **kwargs
    )

    # Close connection
    conn.close()

    pass

# READ ----

def read_forecast_from_database(
    conn_string = "sqlite:///00_database/bike_orders_database.sqlite",
    table_name = "forecast",
    **kwargs
):
    """
    Read a forecast from the database
    
    Args:
        conn_string (str, optional): 
            A slqalchemy connection string to find the database. 
            Defaults to "sqlite:///00_database/bike_orders_database.sqlite".
        table_name (str, optional): 
            The SQL table containing the forecast. Defaults to "forecast".
    
    Returns:
        DataFrame: A pandas data frame with the following columns:
            - id: A unique identifier for the time series
            - date: A date column
            - value: The actual values
            - predictions: The predicted values
            - ci_low: The lower confidence interval
            - ci_high: the upper confidence interval
    """

    # Connect to Database

    engine = sql.create_engine(conn_string)

    conn = engine.connect()

    # Read from table

    df = pd.read_sql(
        f"SELECT * FROM {table_name}",
        con = conn,
        parse_dates= ['date']
    )

    # Close connection

    conn.close()

    return df

# UTILIITIES -----
def convert_to_datetime(data, date_column):

    df_prepped = data

    if df_prepped[date_column].dtype is not 'datetime64[ns]':
        # Try changing to timestamp
        try:
            df_prepped[date_column] = df_prepped[date_column].dt.to_timestamp()
        except:
            try: 
                df_prepped[date_column] = pd.to_datetime(df_prepped[date_column])
            except:
                raise Exception("Could not auto-convert `date_column` to datetime64.")

    return df_prepped
