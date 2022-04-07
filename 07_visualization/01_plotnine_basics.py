# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 7 (Plotnine): Plot Anatomy ----

# Imports
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from my_pandas_extensions.database import collect_data
from my_pandas_extensions.timeseries import summarize_by_time


from plotnine import *

from mizani.formatters import (dollar, dollar_format)

# """ 
#                                     Importing *
#         Imports everything that is in the base directory of the plotnine package.
#         This allows us to import most of the functionality we will need.
        
#                                     Pro-Tip !
#         Many developers will cringe if you import* because it does not specifically tell
#         you which functions are being used in your program.
        
#         We will rectify this as we go through our analysis. 
        
#         Keep in mind, our analysis script is our playground code.
        
#         Our my_pandas_extensions codebase is our production code.
# """

# Data
df = collect_data()
# VISUALIZATION ----

# Step 1: Data Summarization

# """ 
#                                                 Data Summarization 
#             The trick is to know what format your data needs to be in (wide vs long and how to aggregate to get the desired result)

#                                                 Pro-Tip !!
#                                 Visualization is a two step process
                                
#                                 Step 1: Summarize your data (pandas data wrangling)
#                                 Step 2: Visualize your data (plotnine, matplotlib, plotly, altair, bokeh, etc)

# """

# """ 
#             Goal : Plot annual bike sales
#             ! this requires aggregation at a yearly level
            
#             Plotnine requires data in long format (if there are groups involved)
            
#             In this case, tehere are no groups because we are looking at total revenue, so wide and long are the same
# """


bike_sale_y_df = df \
    .summarize_by_time(
        date_column  = "order_date",
        value_column = "total_price",
        rule         = "Y",
        kind = "timestamp"
    )
    
# """ 
# PLOTNINE FORMAT : Needs data in columns

# Right now bike_sale_y_df has order_date as an index, not a column. We need to reset the index.

# """
bike_sale_y_df = df \
    .summarize_by_time(
        date_column  = "order_date",
        value_column = "total_price",
        rule         = "Y",
        kind = "timestamp"
    ) \
        .reset_index()

# Step 2: Plot ---- 
# - Canvas: Set up column mappings | THE CANVAS : is a blank polot that maps your data columns to x-axis and y-axis and any aesthetics like colors and fills 
# - Geometries: Add geoms | GEOMETRIES : These are the main layers that add bars, points , and lines to your plot 
# - Format: Add scales, labs, theme | Scales : can be used to transform the x/y axis

graphic = (
    # Canvas
    ggplot(
        mapping = aes(x = "order_date", y = "total_price"),
        data = bike_sale_y_df     
    )
    
    # Geometries
    + geom_col (fill = "#2C3E50") # + geom_col(fill = "blue")  #  + geom_col(aes(fill = "total_price")) # geom_line()
    + geom_smooth(method = "lm", se = False, color = "dodgerblue") # lm = linear model, se = Standard Error
    
    # Formatting
    + expand_limits(y = [0 , 20e6])
    + scale_y_continuous(labels = dollar_format(big_mark=",", digits = 0))  # (labels = dollar_format(prefix = "€ ", big_mark=",", digits = 0))
    + scale_x_datetime(date_labels = "%Y", date_breaks = "2 years") #Strftime is used in this place for formatting date_labels with yearly format using %Y [String format time]
    + labs(title = "Revenue By Year", x = "", y = "Revenue")
    + theme_minimal()
   
)

graphic


# Saving a plot ----
graphic.save("./07_visualization/bike_sales_yearly.jpg")

# What is a plotnine plot? ----

type(graphic)

graphic.data
graphic.draw