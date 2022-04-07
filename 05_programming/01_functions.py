# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 5 (Programming): Functions ----

# Imports

from charset_normalizer import detect
import pandas as pd
import numpy as np


from my_pandas_extensions.database import collect_data


df = collect_data()

# 1.0 EXAMINING FUNCTIONS ----

# Pandas Series Function
# ?pd.Series.max
# ?np.max

type(df.total_price)

df.total_price.max()



# Pandas Data Frame Function
# ?pd.DataFrame.aggregate

# 2.0 OUTLIER DETECTION FUNCTION ----
# - Works with a Pandas Series

x = df['total_price']

def detect_outliers(x, iqr_multiplier = 1.5, how = "both"):
    """
    Used to detect outliers using the 1.5 IQR Method.

    Args:
        x (Panda Series): A numeric Panda Series
        
        iqr_multiplier (int,float, optional): 
        A Multiplier used to modify the IQR sensitivity. 
        Must be Positive.
        Lower Values will add more outliers.
        Larger Values will add fewer outliers.
        Defaults to 1.5.
        
        how (str, optional): 
        One of "both", "upper" or "lower". Defaults to "both".
        - "both"  : flags both uper and lower outliers.
        - "upper" : flags lower outliers only.
        - "lower" : flags upper outliers only.

    Returns:
        [Panda Series]: A Boolean Series that flags outliers as True/False.
    """
    
    # CHECKS
    
    if type(x) is not pd.Series:
        raise Exception("`x` must be a Panda Series")
    
    if not isinstance(iqr_multiplier, (float,int)):
        raise Exception("`iqr_multiplier` must be an int or a float")
    
    if iqr_multiplier <= 0:
        raise Exception("`iqr_multiplier` must be a positive value")
    
    how_options = ["both", "upper", "lower"]
    
    if how not in how_options:
        raise Exception(
            f"Invalid `how`. Expected value one of {how_options}"
        )
    
    # IQR LOGIC
    
    q75 = np.quantile(x , 0.75)
    q25 = np.quantile(x, 0.25)
    iqr = q75 - q25
    
    lower_limit = q25 - iqr_multiplier * iqr
    upper_limit = q75 - iqr_multiplier *iqr
    
    outliers_upper = x >= upper_limit
    outliers_lower = x <= lower_limit
    
    outliers = outliers_upper | outliers_lower
    
    if how == "both":
        outliers = outliers_upper | outliers_lower
    elif how == "lower":
        outliers = outliers_lower
    else:
        outliers = outliers_upper
    
    return outliers

detect_outliers(df['total_price'], iqr_multiplier = 0.5)

df[detect_outliers(df['total_price'], iqr_multiplier = 0.5)]


# Group By Example

df \
    .groupby("category_2") \
        .apply(
            lambda x: x[
                detect_outliers(x              = x["total_price"],
                                iqr_multiplier = 1.5,
                                how            = "upper")
            ]
        )

# 3.0 EXTENDING A CLASS ----
""" 
Monkey Patching :

We can add a method by a process called "monkey patching", which simply just adds a method at runtime.

It's a convenient way to extend a python class.

Caution: We need to be careful not to overwrite existing classes when we do this.
"""

pd.Series.detect_outliers = detect_outliers



