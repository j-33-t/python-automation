# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 3 (Pandas Core): Data Structures ----

# IMPORTS ----

import pandas as pd
import numpy as np

from my_pandas_extensions.database import collect_data


df = collect_data()


# 1.0 HOW PYTHON WORKS - OBJECTS

# Objects

type(df)

# Objects have classes
type(df).mro()

type("apple").mro()




# Objects have attributes (in VS code they are displayed as wrench icon)

df.shape # shape returns no of rows and columns
df.columns
df.dtypes

# Objects have methods (in VS code they are displayed as cube icon)

df.query("model == 'Jekyll Carbon 2'")

df["price"].describe()

# 2.0 KEY DATA STRUCTURES FOR ANALYSIS

# - PANDAS DATA FRAME

type(df)


# - PANDAS SERIES

type(df["order_date"])

df["order_date"].dt.year  #attribute dt.year 

# - NUMPY ARRAY

type(df["order_date"].values)

type(df["order_date"].values).mro()


# 3.0 DATA STRUCTURES - PYTHON

# Data Types

type(df["price"].values)

df["price"].values.dtype

df["order_date"].values.dtype


# Dictionaries

d = {'a' : 1, 'b': 2}
type(d)

d.keys()
d.values()

d["a"]

# Lists
a = [5,"apple", [2,"B"]]

a[0]
a[1]
a[2]

list(d.values())[0]
list(d.values())[1]


# Tuples

df.shape
type(df.shape)

t = (10,20)
t[0] = 20  #immutable object does not support item assignment



# Base Data Types

type(1.5)
type(1)
type("a")
type(True)

df.total_price.dtype

type(df["model"].values[0])


# Casting (Converting data from one type to another)

model = "Jekyll Carbon 2"
price = 6070

f"The first model is: {model}"

f"The price of the first model is: {price} "

price + "Some text" #Error

str(price) + " Some Text"


# Generator
"""
    It produces a specification for how to generate 
    a sequqnce. This is a memory saving strategy
    that only creates the range when you need it.
"""

r = range(1,11)

type(r)

# Casting to a list, array, to series, to dataframe 
# (casting a range from low to high)

list(r)

np.array(r)

pd.Series(r)

pd.Series(r).to_frame()



# DATAFRAME COLUMN DATA TYPE (dtype) Conversion 

"""

The principles of data cleaning is derived from your ability
to convert columns of data to the appropriate data type (dtype)
for your analysis.

"""
df["order_date"].dtype

df["order_date"].astype('str').str.replace("-", "/")
