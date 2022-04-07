# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 9 (Jupyter Automated Reporting): Papermill Automation ----

# IMPORTS ----
import pandas as pd
import numpy as np
import pathlib
import os

import papermill as pm

from my_pandas_extensions.database import read_forecast_from_database
# COLLECT DATA ----
df = read_forecast_from_database()

# 1.0 SELECTING REPORT ID'S ----
ids = df['id'].unique()

ids = pd.Series(ids)

ids_total = ids[ids.str.startswith('Total')]
ids_cat_1 = ids[ids.str.startswith('Category 1')]
ids_cat_2 = ids[ids.str.startswith('Category 2')]
ids_bikeshop = ids[ids.str.startswith('Bikeshop')]

id_sets = [list(ids_total),
           list(ids_cat_1),
           list(ids_cat_2),
           list(ids_bikeshop)]

# id_sets[0]
# id_sets[1]

id_sets

# 2.0 SETUP DIRECTORY ----
directory = "./09_jupyter_papermill/reports/"

dir_path = pathlib.Path(directory)

str(dir_path.absolute())

dir_path.name

# Make the report directory if doesn't already exist

os.mkdir(dir_path)

# check if dir exists
os.path.isdir(dir_path)
os.path.isdir("test")

directory_exists = os.path.isdir(dir_path)

if not directory_exists:
    print(f"Makeing directory at {str(dir_path.absolute)}")
    os.mkdir(dir_path)

# 3.0 MAKE JUPYTER TEMPLATE ----
# - Convert Analysis to a Papermill Template
# - Parameterize key variables:
#   - ids
#   - title
#   - data: Note that data will be passed as json

# #############################################################################
#                             PRO-TIP !!                                      #
#         When building a loop, it's a good idea to break it up in 2 steps:   #
#             1. Iterating without a loop                                     #
#             2. Migrating code into a loop                                   #
#                                                                             #
#         This helps to give maximum control over the loop design.            #
#                                                                             #
# #############################################################################

# 4.0 PAPERMILL ----

# Key Variable
i = 0

template_path = pathlib.Path("./09_jupyter_papermill/template/01_jupyter_analysis_template.ipynb")

# Report Output Path Automation 
output_path = pathlib.Path(f"./09_jupyter_papermill/reports/sales_report_{i}.ipynb")

params = {
    "ids": id_sets[i],
    "title": f"Sales Report {i + 1}",
    "data": df.to_json()
}

###############################################################################
#                             PRO-TIP !!                                      # 
#         Any Time you convert data from JSON (or get data from SQL Database) #  
#                        Always check the format.                             #
#         Sometimes you may not get equivalent objects back due to the        #
#         conversion process.                                                 #
#                                                                             #
#         Specifically check that dates are formatted properly                #
#                                                                             #
###############################################################################

# data = df.to_json()
# data_from_json = pd.read_json(data) #there is extra option to convert date in pd.read_json [convert_dates = True]

# data_from_json.info()

# Iterating without a loop

pm.execute_notebook(
    input_path  = template_path,
    output_path = output_path,
    parameters  = params,
    report_mode = True
)


# Iterating with for-loop and enumerate()

for i, id_set in enumerate(id_sets):
    
    template_path = pathlib.Path("./09_jupyter_papermill/template/01_jupyter_analysis_template.ipynb")

    # Report Output Path Automation 
    output_path = pathlib.Path(f"./09_jupyter_papermill/reports/sales_report_{i}.ipynb")

    params = {
        "ids": id_set,
        "title": f"Sales Report {i + 1}",
        "data": df.to_json()
    }
    
    pm.execute_notebook(
    input_path  = template_path,
    output_path = output_path,
    parameters  = params,
    report_mode = True
    )
