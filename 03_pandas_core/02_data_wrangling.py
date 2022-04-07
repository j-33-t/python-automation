# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Week 2 (Data Wrangling): Data Wrangling ----

# IMPORTS
from xml.etree.ElementInclude import include
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core import groupby
from sqlalchemy import asc

from my_pandas_extensions.database import collect_data


# DATA
df = collect_data()


# 1.0 SELECTING COLUMNS

# Select by name
""" 
Subsetting data frame columns with a list of names

df['order_date'] # Single brackets return a series

df[['order_date]] # Double brackets returns a dataframe
"""

["order_date", "order_id", "order_line"]


df[["order_date", "order_id", "order_line"]]


# Select by position
df.iloc[:, 1]   # [row, column]
df.iloc[:, 0:3] 


# Select by text matching
""" 
Mostly used regex expression

"text"
"^text" = ^ is used to match string beginning with the word "text"
"text$" = $ is used to match string ending with the word "text"
(text1)|(text2) = | is used for "text1" or "text2"
"^text$" = Matches string beginning and ending with word "text"
"^(?!text$).*" = Matches strings except the string "text"

"""

df.filter(regex = "(^model)|(^cat)", axis = 1)

df.filter(regex = "^(?!order_line).*", axis = 1)


# Rearranging columns

""" 
index.tolist() , it converts a column or row index to a list, which is iterable

*l  = is used for list unpacking, converts a nested list to a unnested list
"""

""" 
REARRANGING A SINGLE COLUMN
"""
l = df.columns.tolist()

l.remove("model")

l

df[['model', *l]]

""" 
REARRANGING MULTIPLE COLUMNS - REPETITIVE WAY
"""
l = df.columns.tolist()
l

l.remove('model')
l.remove('category_1')
l.remove('category_2')

df[['model', 'category_1', 'category_2', *l]]

""" 
REARRANGING MULTIPLE COLUMNS - MULTIPLE WAY  - LIST COMPREHENSION

"""
l = df.columns.tolist()
l
cols_to_front = ["model", "category_1", "category_2"]

l2 = [col for col in l 
      if col not in cols_to_front]

df[[*cols_to_front, *l2]]

# Select by data types
df.info()
df1 = df.select_dtypes(include = 'object')
df2 = df.select_dtypes(exclude='object')

pd.concat([df1, df2], axis = 1)



# Dropping Columns (De-selecting)

df.drop(['model', 'category_1', 'category_2'], axis = 1)

# 2.0 ARRANGING ROWS ----

""" 
df.sort_values() : Great for sorting by a column.
Can sort by Multiple Columns to get group wise sort
"""

df.sort_values("price", ascending = False)

df.sort_values("order_date", ascending = False)

df['price'].sort_values(ascending= False)


# 3.0 FILTERING  ----

# Simpler Filters [using booleans output]

df.order_date >= pd.to_datetime("2015-01-01")

df[df.order_date >= pd.to_datetime("2015-01-01")]

df.model == "Trigger Carbon 1"

df[df.model == "Trigger Carbon 1"]

df.model.str.startswith("Trigger")

df[df.model.str.startswith("Trigger")]

df[df.model.str.contains("Carbon")]

# Query [@ can be used to mention a variable]

price_threshold_1 = 9000
price_threshold_2 = 1000

df.query("price >= @price_threshold_1")

df.query("(price >= @price_threshold_1)|(price <= @price_threshold_2)")

df.query(f"price >= {price_threshold_1}")


# Filtering Items in a List

df['category_2'].unique()

df['category_2'].value_counts()

df[df["category_2"].isin(['Triathalon','Over Mountain'])]

# ~ is used to negate , ie is not in 
df[~ df["category_2"].isin(['Triathalon','Over Mountain'])]

# Slicing
df[:5]

df.head(5)
df.tail(5)


# Index Slicing
df.iloc[0:5]
df.iloc[0:5, [1,3,5]]
df.iloc[:,[1,3,5]]

# Unique / Distinct Values
df[['model', 'category_1', 'category_2','frame_material']] \
    .drop_duplicates()
    
df['model'].unique()

# Top / Bottom
df.nlargest(n = 20, columns = 'total_price')

df['total_price'].nlargest(n = 20)

df.nsmallest(n = 20, columns= 'total_price')

df['total_price'].nsmallest(n = 20)

# Sampling Rows

""" 
df.sample() : Select random rows.

Good for train/test splitting. 
Use random_state to make reproducible.

"""

df.sample(n = 10, random_state=123)

df.sample(frac = 0.10, random_state=123)

df.sample(frac = 0.90, random_state=123)

# 4.0 ADDING CALCULATED COLUMNS (MUTATING) ----


# Method 1 - Series Notations
""" 
df.copy() : Makes a copy of the data frame
            so we don't accidently overwrite it
"""

df2 = df.copy()

df2['new_col'] = df2['price'] *df2['quantity']

df2['new_col_2'] = df['model'].str.lower()


# Method 2 - assign (Great for method chaining)

""" 
Lambda Function
A function made on the fly that has no name. It's 
sometimes called an "Anonymous Function"

Example:

def price_quantity(x):
    return x.price *x.quantity
    
Can be converted into a short hand lambda function:

lambda x: x.price* x.quantity


Why do we use Lambda Functions ?

- Less code, easier to read, don't need to think about what 
to name it.

'x' in lambda is the incoming dataframe, you will grab series
from x and modify them using transformations
"""

df['frame_material'].str.lower()

df.assign(frame_material = lambda x: x["frame_material"].str.lower())


df.assign(frame_material_lower = lambda x: x["frame_material"].str.lower())


""" 
dropping duplicates has the effect of generating our bikes
table that identifies the unique bike models and their
prices
"""
df[["model", "price"]] \
    .drop_duplicates() \
        .set_index('model') \
            .plot(kind = 'hist')
plt.show()


""" 
The bell-shaped distribution is better for certain models
like linear regression. It will help in improve model

"""


df[["model", "price"]] \
    .drop_duplicates() \
        .assign(price = lambda x: np.log(x['price'])) \
        .set_index('model') \
            .plot(kind = 'hist')
plt.show()

# Adding Flags (True/False)

"Supersix Evo Hi-Mod Team".lower().find("supersix") >= 0

"Beast of the East 1".lower().find("supersix") >= 0

""" 
Pandas Series has the str.contains() method, which simplifies
text searching so we don't need to use find() >= 0

Common Error: ATTRIBUTE ERROR
A super common error is to forget to add a "str" for the string
accessor. 

if you forget "str" accessor, you'll get an "Attribute Error"
, which is a way of saying your series does not have an 
attribute "contains()".
"""

df['model'].str.lower().str.contains("supersix")

df.assign(flag_supersix = lambda x: x["model"].str.lower().str.contains("supersix"))

# Binning

""" 
A great way to convert numeric data to groups based on their values.

Example: Converting a list of job tenure to ranges

There are tow main types:
1) Even-Width Binning, pd.cut()
2) Quantile Binnig, pd.qcut()
"""

pd.cut(df.price, bins = 3)

df[['model', 'price']] \
    .drop_duplicates() \
        .assign(price_group = lambda x: pd.cut(x.price, bins = 3 )) \
            .pivot(
                index = "model",
                columns= "price_group",
                values = "price"
                
            ) \
                .style.background_gradient(cmap = 'Blues')


""" 
Pandas DF Style Accessor

Data Frames have a style accesor that is not so commonly
used. 

It is really powerful for making tables for html and excel
reports.

"""

pd.qcut(df.price, q = [0, 0.33, 0.66, 1], labels = ['low', 'medium', 'high'])



# 5.0 GROUPING  ----

# 5.1 Aggregations (No Grouping)

""" 
Summarizing (Aggregating) : Applying a summary function that
takes a Series and returns a single value

Example: np.mean(), .count(), 

Summarizing differs from "transformations" like np.log() and pd.qcut(),
which returns a series of the same length as the input

"""

df.sum()

df[['total_price']].sum().to_frame()

df \
    .select_dtypes(exclude= ['object']) \
        .drop('order_date', axis = 1) \
            .sum()


df.agg(np.sum)

df \
    .select_dtypes(exclude= ['object']) \
        .drop(['order_date', 'order_id', 'order_line'], axis = 1) \
    .agg([np.sum , np.mean, np.std, np.var])
    
df.agg(
    {
        'quantity': np.sum,
        'total_price': [np.sum, np.mean, np.std]
    }
)
    
    
# Common Summaries

df['model'].value_counts()

df[['model']].value_counts()

df.nunique()


df.isna().sum()


# 5.2 Groupby + Agg

df.groupby(['city', 'state']) \
    .agg(
        {
            "total_price" : np.sum,
            "quantity": np.sum
        }
    ) \
        .sort_values(by = "total_price", ascending= False)


# Get the sum and median by groups
""" 
PRO TIP !!!!

Follow this process when doing a groupby:

1. Isolate just the columns needed for the analysis
2. Group By the Grouping Column(s).
3. Apply the aggregation/summarization.
4. Reset Index if needed
"""

summary_df_1 = df[["category_1", "category_2", "total_price"]] \
    .groupby(["category_1", "category_2"]) \
        .agg([np.sum, np.median]) \
            .reset_index()

# Apply Summary Functions to Specific Columns

summary_df_2 = df[["category_1", "category_2", "total_price","quantity"]] \
    .groupby(["category_1", "category_2"]) \
        .agg({
            "quantity": np.sum,
            "total_price": np.sum
        }) \
            .reset_index()

# Detecting NA

summary_df_1.columns

summary_df_1.isna().sum()

# 5.3 Groupby + Transform (Apply)
# - Note: Groupby + Assign does not work. No assign method for groups.

""" 
resample() is just another way to group.
We are grouping on a weekly group in addition to by Category 2.

Then we tell our aggregation to apply the sum() to these groups.
"""

summary_df_3 = df[["category_2","order_date", "total_price", "quantity"]] \
    .set_index("order_date") \
        .groupby("category_2") \
            .resample("W") \
                .agg(np.sum) \
                    .reset_index()
                    

summary_df_3 \
    .set_index('order_date') \
        .groupby('category_2') \
            .apply(lambda x: (x.total_price - x.total_price.mean() ) / x.total_price.std() ) \
                .reset_index() \
                    .pivot(
                        index = "order_date",
                        columns = "category_2",
                        values = "total_price"
                    ) \
                        .plot()
plt.show()


summary_df_3 \
    .set_index(['order_date', 'category_2']) \
        .groupby('category_2') \
            .apply(lambda x: (x - x.mean()) / x.std()) \
                .reset_index()


# 5.4 Groupby + Filter (Apply)

summary_df_3 \
    .groupby('category_2') \
        .tail(5)
        
        
summary_df_3 \
    .groupby('category_2') \
        .apply(lambda x: x.iloc[10:20])
        
summary_df_3 \
    .groupby('category_2') \
        .apply(lambda x: x.iloc[-20:])

# 6.0 RENAMING ----

# Single Index

summary_df_2 \
    .rename(columns = {'category_1' : 'Category 1' })
    
summary_df_2.columns.str.replace("_", " ").str.title()
    
summary_df_2 \
    .rename(columns = lambda x: x.replace("_", " ").title())

# Targeting specific columns
summary_df_2 \
    .rename(columns = {
        "total_price": "Revenue"
    })

# - Mult-Index
summary_df_1.columns

summary_df_1 \
    .set_axis(["A","B","C","D"], axis = 1)
    
"""
LIST COMPREHENSION for multi index renaming
"""
"_".join(("total_price", "median"))

["_".join(col) for col in summary_df_1.columns.tolist()]

summary_df_1 \
    .set_axis(
        ["_".join(col) for col in summary_df_1.columns.tolist()],
        axis = 1)


# 7.0 RESHAPING (MELT & PIVOT_TABLE) ----

# Aggregate Revenue by Bikeshop by Category 1 
"""
Pivoting is normally done after you've summarized data
So we'll quickly make a summary dataset to work with.
"""

bikeshop_revenue_df = df[["bikeshop_name", "category_1", "total_price"]] \
    .groupby(["bikeshop_name", "category_1"]) \
        .sum() \
            .reset_index() \
                .sort_values("total_price", ascending= False) \
                    .rename(columns = lambda x: x.replace("_", " ").title())


# 7.1 Pivot & Melt 

# Pivot (Pivot Wider)

bikeshop_revenue_wide_df = bikeshop_revenue_df \
    .pivot(
        index = ["Bikeshop Name"],
        columns = ["Category 1"],
        values = ["Total Price"]
    ) \
        .reset_index() \
            .set_axis(
                ["Bikeshop Name", "Mountain", "Road"],
                axis = 1
            )
            
bikeshop_revenue_wide_df\
    .sort_values("Mountain") \
    .plot(
    x = "Bikeshop Name",
    y = ["Mountain"],
    kind = "barh"
    )
    
plt.show()


bikeshop_revenue_wide_df\
    .sort_values("Mountain") \
    .plot(
    x = "Bikeshop Name",
    y = ["Mountain", "Road"],
    kind = "barh"
    )
    
plt.show()

""" 
Pandas has a number of Styling Options that can be used 
to improve the output
"""

bikeshop_revenue_wide_df \
    .sort_values("Mountain", ascending= False) \
        .style \
            .highlight_max() \
                .format(
                    {
                        "Mountain" : lambda x: "$" + str(x)
                    }
                )
                
""" Formatting using mizani package """

from mizani.formatters import dollar_format

usd = dollar_format(prefix= "$", digits=0, big_mark=",")

usd([1000, 2000])
usd([1000, 2000])[0]

bikeshop_revenue_wide_df \
    .sort_values("Mountain", ascending= False) \
        .style \
            .highlight_max() \
                .format(
                    {
                        "Mountain" : lambda x: usd([x])[0],
                        "Road" : lambda x: usd([x])[0]
                    }
                ) \
                    .to_excel("03_pandas_core/bikeshop_revenue_wide.xlsx")

# Melt (Pivoting Longer)

bikeshop_revenue_long_df = pd.read_excel("./03_pandas_core/bikeshop_revenue_wide.xlsx") \
    .drop(columns= "Unnamed: 0") \
        .melt(
            value_vars = ["Mountain", "Road"], 
            var_name   = "Category 1", 
            value_name = "Revenue",
            id_vars    = "Bikeshop Name"
        )

from plotnine import (ggplot, aes, 
                      geom_col, facet_wrap,
                      theme_minimal, coord_flip)

    

ggplot(
    mapping = aes(x = "Bikeshop Name", y = "Revenue", fill = "Category 1"),
    data = bikeshop_revenue_long_df) + \
    geom_col() + \
    coord_flip() + \
    facet_wrap("Category 1")
    
""" 
Sorting by Bikeshop Name
by coverting the column data into categorical variable

----CATEGORICAL DATA TYPE-----
We use this when we want to sort text data.
Categorical data combines a label(text) and a
numeric value (numeric order)

Key Concept !!!

We need to sort the Bikeshop Name by the Revenue.
We can do this by making Bikeshop Name a categorical
with levels (numeric values ) that are ordered by the revenue

"""

bikeshop_order = bikeshop_revenue_long_df \
    .groupby("Bikeshop Name") \
        .sum() \
            .sort_values("Revenue") \
                .index \
                    .tolist()
                    
bikeshop_revenue_long_df["Bikeshop Name"] = pd.Categorical(
    bikeshop_revenue_long_df["Bikeshop Name"],
    categories = bikeshop_order # we need this to rank categories
)

bikeshop_revenue_long_df.info() # Now it is categorical

ggplot(
    mapping = aes(x = "Bikeshop Name", y = "Revenue", fill = "Category 1"),
    data = bikeshop_revenue_long_df) + \
    geom_col() + \
    coord_flip() + \
    facet_wrap("Category 1") + \
    theme_minimal()
    

# 7.2 Pivot Table (Pivot + Summarization, Excel Pivot Table)

""" 
df.pivot_table() :  Converts raw data into summarized tables by
                    combining pivoting and aggregation into 1 function.
                
"""

df \
    .pivot_table(
        columns = None,
        values  = "total_price",
        index   = "category_1",
        aggfunc = np.sum
    )

df \
    .pivot_table(
        columns = "frame_material",
        values  = "total_price",
        index   = "category_1",
        aggfunc = np.sum
    )
    
df \
    .pivot_table(
        columns = None,
        values  = "total_price",
        index   = ["category_1", "frame_material"],
        aggfunc = np.sum
    )
    
sales_by_cat1_cat2_year_df = df \
    .assign(year = lambda x: x.order_date.dt.year) \
    .pivot_table(
        index = ["category_1", "category_2"],
        aggfunc= np.sum,
        columns= "year",
        values = "total_price"
    )
    
    
# 7.3 Stack & Unstack ----

# Unstack - Pivots Wider 1 Level (Pivot)


sales_by_cat1_cat2_year_df \
    .unstack(
        fill_value = 0
    )
    
sales_by_cat1_cat2_year_df \
    .unstack(
        level = 0,
        fill_value = 0
    )

sales_by_cat1_cat2_year_df \
    .unstack(
        level = "category_1",
        fill_value = 0
    )

sales_by_cat1_cat2_year_df \
    .unstack(
        level = "category_2",
        fill_value = 0
    )

# Stack - Pivots Longer 1 Level (Melt)

sales_by_cat1_cat2_year_df \
    .stack(
        level = "year"
    )
    
sales_by_cat1_cat2_year_df \
    .stack(
        level = "year"
    ) \
        .unstack(
            level = ["category_1", "category_2" ]
        )

# 8.0 JOINING DATA ----

orderlines_df = pd.read_excel("./00_data_raw/orderlines.xlsx").drop(columns= "Unnamed: 0")
bikes_df = pd.read_excel("./00_data_raw/bikes.xlsx")

# Merge (Joining)
""" 
Joining :   We join data frames to get data from one data frame
            into another, where there is primary key relationship.
            
            99% of the time we can use "LEFT JOIN".
"""
pd.merge(
    left     = orderlines_df,
    right    = bikes_df,
    left_on  = "product.id",
    right_on = "bike.id"
)

# Concatenate (Binding)

# Columns 
df_1 = df.iloc[:, :5]
df_2 = df.iloc[:, -5:]

"""
They need to have same indexing otherwise they will show NaN
"""

pd.concat(
    [df_1 , df_2],
    axis = 1
)


# Rows 
df_1 = df.head(5)
df_2 = df.tail(5)

pd.concat([df_1, df_2], axis = 0)


# 9.0 SPLITTING (SEPARATING) COLUMNS AND COMBINING (UNITING) COLUMNS

# Separate

df_2 = df['order_date'].astype('str').str.split("-", expand = True) \
    .set_axis(["year", "month", "day"], axis = 1)
    
df_2 = df_2.astype('int')

pd.concat([df, df_2], axis = 1)

# Combine

df_2 = df_2.astype('str')

df_2.info()

df_2['year'] + "-" + df_2['month'] + "-" + df_2['day'] 

# 10.0 APPLY 
# - Apply functions across rows 


sales_cat2_daily_df = df[["category_2", "order_date", "total_price" ]] \
    .set_index("order_date") \
        .groupby("category_2") \
            .resample("D") \
                .sum()
                
np.mean([1,2,3]) # Aggregation

np.sqrt([1,2,3]) # Transformation

sales_cat2_daily_df.apply(np.mean)
sales_cat2_daily_df.apply(np.sqrt)



""" 
Broadcasting :  Simply attaching an aggregation or smaller array to the size
                of a larger array.
                
                This is also called "recycling" and can be performed with 
                np.repeat()
"""

sales_cat2_daily_df.apply(np.mean, result_type = "broadcast")  # Method 1
sales_cat2_daily_df.apply(lambda x: np.repeat(np.mean(x), len(x))) # Method 2

sales_cat2_daily_df \
    .groupby("category_2") \
        .apply(np.mean)
        
sales_cat2_daily_df \
    .groupby("category_2") \
        .apply(lambda x : np.repeat(np.mean(x), len(x)))
        
        
# Grouped Broadcast - Use transform

sales_cat2_daily_df \
    .groupby("category_2") \
        .transform(np.mean)
        
sales_cat2_daily_df \
    .groupby("category_2") \
        .transform(np.sqrt)


# 11.0 PIPE 
# - Functional programming helper for "data" functions

"""
df.pipe() : A functional programming helper designed to make it easier to 
            method chain functions that you create that modify data frames.

-- Custom function---
add.columns():  This is a minimal function we'll create that acts like df.assign()
                by adding calculated columns. 
                
                Then we'll show how we can method chain with df.pipe()

"""

data = df


def add_column(data, **kwargs):
    
    data_copy = data.copy()
    
    # print(kwargs)
    
    data_copy[list(kwargs.keys())] = pd.DataFrame(kwargs)
    
    return data_copy

add_column(df, total_price_2 = df.total_price * 2)


df \
    .pipe(
        add_column, 
        category_2_lower = df["category_2"].str.lower()
          )
