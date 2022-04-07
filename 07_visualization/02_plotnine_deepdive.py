# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 7 (Plotnine): Plotnine Deep-Dive ----
# """ 
#                                 Plotnine Deep-Dive
#             Now we're ready to buld many of the most common plots you will use:
            
#                 Scatter Plots
#                 Line Plots
#                 Bar/ Column Plot
#                 Historgram/ Density
#                 Box and Violin Plots
#             This section is a Cookbook for building common plots.
# """


# Imports
from itertools import groupby
import pandas as pd
import numpy as np
import matplotlib

import matplotlib.pyplot as plt

from my_pandas_extensions.database import collect_data
from my_pandas_extensions.timeseries import summarize_by_time


from plotnine import *

from mizani.formatters import (dollar, dollar_format)

# Matplotlib stylings


# Data
df = collect_data()


# 1.0 Scatter Plots ----
# - Great for Continuous vs Continuous [Exposes relationships between variables]

# Goal: Explain relationship between order line value
#  and quantity of bikes sold

                        # Step 1: Data Preparation 
quantity_total_price_by_order_df = df[["order_id", "quantity", "total_price"]] \
    .groupby("order_id") \
        .sum() \
            .reset_index()

                        # Step 2 : Visualization 
(
    ggplot(
        # Canvas
        mapping = aes(x = "quantity", y = "total_price"),
        data = quantity_total_price_by_order_df
        
    )
        # Geometry
        + geom_point(alpha = 0.5 )  # to adjust opacity of points we can use alpha 
        + geom_smooth(method = "lm") # A great way to expose the trend between two continuous variables. 
)



# 2.0 Line Plot ----
# - Great for time series

# Goal: Describe revenue by Month, expose cyclic nature

# Step 1: Data Manipulation [Pro-Tip : ggplot only supports kind = "timestamp"]

bike_sales_m_df = df \
    .summarize_by_time(
        date_column  = "order_date",
        value_column = "total_price",
        rule         = "M",
        kind         = "timestamp"
    ) \
        .reset_index()
    

# Step 2: Plot

(
    ggplot(
       
        #Canvas
        mapping = aes(x = "order_date", y = "total_price"),
        data = bike_sales_m_df
    )
    
        # Geometry
    + geom_line()
    + geom_smooth(method = "lm", se = False) 
    + geom_smooth(method = "loess", se = False, span = 0.22, color = "dodgerblue")
)



# 3.0 Bar / Column Plots ----
# - Great for categories

# Goal: Sales by Descriptive Category

# Step 1: Data Manipulation

from plydata.cat_tools import cat_reorder

bike_sales_cat2_df = df \
    .groupby("category_2") \
        .agg(
            {"total_price" : np.sum}
            ) \
                .reset_index()


# Aside: Categorical Data (pd.Categorical)
# """ 
#     Ordering is off in the charts with the above table even after sorting. 
#     Generally we want the order to follow the magnitude of the bar. How can we do this ?
    
#                     Pandas Categorical 
#         A special date type that combines a text label with a numeric ordering.
#         First we import cat_reorder from plydata.cat_tools.

#                     Ordering Categories
#         We want to have "Cross Country Race" be in the first position because it has the largest total_price.
#         "Elite Road" should be ranked in 2nd position and so on.
        
#                     cat_reorder()
#         Convert a categorical or text column to a categorical column with a numeric order derived from a numeric column.
        
            
#             Key Concept!!
#         Categorical Data has "codes" which is a numeric ordering. Zero is first.
#         Categorical Data also has "labels", which is the text based category name.       
        
# """

bike_sales_cat2_df = df \
    .groupby("category_2") \
        .agg(
            {"total_price" : np.sum}
            ) \
                .reset_index() \
                    .sort_values(by = "total_price", ascending = False) \
                    .assign(
                        category_2 = lambda x: cat_reorder(
                            x["category_2"],
                            x["total_price"]#,
                            #ascending = False # Use it to flip the reordering in the chart
                        )
                    ) 

bike_sales_cat2_df.category_2.cat.codes

# - Used frequently in plotting to designate order of categorical data



# Step 2: Plot

# - Plotting without ranking

(
    ggplot(
        mapping = aes(x = "category_2", y = "total_price"),
        data = bike_sales_cat2_df
    ) + 
    geom_col(fill = "#2c3e50") +
    coord_flip() +
    theme_minimal()
)


# 4.0 Histogram / Density Plots ----
# - Great for inspecting the distribution of a variable

# Goal: Unit price of bicycles

# Histogram ----

# Step 1: Data Manipulation

unit_price_by_frame_df = df[["model", "frame_material", "price"]] \
    .drop_duplicates()


# Step 2: Visualize
g_canvas = (
    ggplot(
        #Canvas
        mapping = aes("price"),
        data = unit_price_by_frame_df
    )
)

# Geometry 1
g1 = (g_canvas 
    + geom_histogram(bins = 13, color = "white", fill = "#2c3e50")
)

# Geometry 2 - filling by frame_material

g_canvas = (
    ggplot(
        #Canvas
        mapping = aes(x = "price", fill = "frame_material"),
        data = unit_price_by_frame_df
    )
)

g2 = (g_canvas 
    + geom_histogram(bins = 13, color = "white")
)

# Facets -  adding more layers

# side by side facets
g2 + facet_grid(facets=[".", "frame_material"])

#stacked facets : Advantage here is we can compare the plots because they share the x axis
g2 + facet_grid(facets=["frame_material" , "."]) + theme_minimal()

# Density ----

# """ 
#                             Density Plot
#             Converts a numeric variable to a probability density
#             you'll see this referred to as kernal Density Estimation (KDE) plots. 
            
#                             Why use Density?
#             Density for the most part is "non-parametric"
#             meaning you don't need to adjust the parameters like you do with 
#             histograms with the bins.
            
#             But sometimes density can get waves, in which case you can make adjustments.
# """

g_canvas + geom_density(alpha = 0.5)


# 5.0 Box Plot / Violin Plot ----
# - Great for comparing distributions

# Goal: Unit price of model, segmenting by category 2

# Step 1: Data Manipulation

unit_price_cat2_df = df[["category_2", "model", "price"]] \
    .drop_duplicates() \
        .assign(category_2 = lambda x: cat_reorder(
            x["category_2"], 
            x["price"], 
            fun = np.median, 
            ascending= True
        ))

# Step 2: Visualize

# Box Plot
(
    ggplot(mapping = aes( "category_2", "price"),
           data = unit_price_cat2_df)
    + geom_boxplot()
    + coord_flip()
)


# Violin Plot & Jitter Plot

(
    ggplot(mapping = aes( "category_2", "price"),
           data = unit_price_cat2_df)
    + geom_violin()
    + geom_jitter(width = 0.15 , alpha = 0.5) # Adds a small amount of random to the points , TIP! : Use the width parameter to adjust the amount of variability
    + coord_flip()
)

# 6.0 Adding Text & Label Geometries----

# Goal: Exposing sales over time, highlighting outlier

# Data Manipulation

usd = dollar_format(prefix = "$", big_mark = ",", digits = 0)
usd([100, 1000, 1e10])
 

bike_sales_yd_df = df \
    .summarize_by_time(
        date_column  = "order_date",
        value_column = "total_price",
        rule         = "Y"
    ) \
        .reset_index() \
            .assign(
                total_price_text = lambda x: usd(x["total_price"])
            )



# Adding text to bar chart
# Filtering labels to highlight a point

(
    ggplot(
        # Canvas
        mapping = aes(x = "order_date", y = "total_price"),
        data = bike_sales_yd_df
    )
    
        # Geometry
    + geom_col(fill = "#2c3e50")
    + geom_smooth(method = "lm", se = False, color = "dodgerblue")
    + geom_text(aes(label = "total_price_text"),
                va        = "top", 
                size      = 8, 
                nudge_y   = -1.2e5, 
                color     = "white")
    + geom_label(
        label   = "Major Demand",
        color   = "red",
        nudge_y = 1e6,
        size    = 10,
        data    = bike_sales_yd_df[
            bike_sales_yd_df.order_date.dt.year == 2013
        ]
    )
    
    + expand_limits(y = [0, 20e6])
    + scale_x_datetime(date_labels = "%Y")
    + scale_y_continuous(labels = usd)
)


# 7.0 Facets, Scales, Themes, and Labs ----
# - Facets: Used for visualizing groups with subplots
# - Scales: Used for transforming x/y axis and colors/fills
# - Theme: Used to adjust attributes of the plot
# - Labs: Used to adjust title, x/y axis labels

# Goal: Monthly Sales by Categories

# Step 1: Format Data

bike_sales_cat2_m_df = df \
    .summarize_by_time(
        date_column = "order_date",
        value_column = "total_price",
        groups = "category_2",
        rule = "M",
        wide_format = False
    ) \
        .reset_index()

# Step 2: Visualize

matplotlib.pyplot.style.available
matplotlib.pyplot.style.use("seaborn")

g = (
    ggplot(
        
        #Canvas
        mapping= aes(x = "order_date", y = "total_price", color = "category_2"),
        data = bike_sales_cat2_m_df
    )
        # Geometry
    + geom_line()
    + geom_smooth(method = "loess", se = False, span = 0.2, color = "dodgerblue")
    
        # Formatting
    + facet_wrap(facets="category_2", ncol = 3, scales = "free_y")
    + scale_x_datetime(date_labels = "%Y", date_breaks = "2 Years")
    + scale_y_continuous(labels = usd)
    + scale_color_cmap_d()
    + theme_matplotlib()
    + theme(
        strip_background = element_rect(fill = "cyan"),
        legend_position = "none",
        figure_size= (16,8),
        subplots_adjust= {"wspace": 0.25}
    )
    + labs( title = "Revenue by Month and Category 2")
)

g.save("./07_visualization/bike_sales_cat2_m.jpg")






