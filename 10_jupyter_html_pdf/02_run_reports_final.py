# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 10 (Jupyter Automated Reporting, Part 2): Run Reports, Version 2 ----

# IMPORTS ----

import pathlib
import os
import string

import pandas as pd
import numpy as np

import papermill as pm

from my_pandas_extensions.database import read_forecast_from_database

# >>> ADD IMPORTS <<<


# COLLECT DATA ----

df = read_forecast_from_database()

# SELECTING REPORT ID'S ----
ids = df['id'].unique()
ids = pd.Series(ids)

ids_total = ids[ids.str.startswith('Total')]
ids_cat_1 = ids[ids.str.startswith('Category 1')]
ids_cat_2 = ids[ids.str.startswith('Category 2')]
ids_bikeshops = ids[ids.str.startswith('Bikeshop')]

id_sets = [
    list(ids_total),
    list(ids_cat_1),
    list(ids_cat_2),
    list(ids_bikeshops)
]

id_sets


# REPORT TITLES ----

titles = [
    "Sales Forecast: Total Revenue",
    "Sales Forecast: Category 1",
    "Sales Forecast: Category 2",
    "Sales Forecast: Bikeshops"
]

titles


# TEMPLATE INPUT PATH ----

def get_template_path(path='09_jupyter_papermill/template/jupyter_report_template.ipynb'):
    return path

get_template_path()


# 1.0 MODIFY REPORTING FUNCTION ----
# - Upgraded Reporting Function: Version 2
# - Add HTML and PDF reporting

def run_reports(data, id_sets=None, 
                report_titles = None,
                directory = "reports/",
                covert_to_html = False, 
                convert_to_pdf = False):

    # Make the directory if not created

    dir_path = pathlib.Path(directory)
    directory_exists = os.path.isdir(dir_path)
    if not directory_exists:
        print(f"Making directory at {str(dir_path.absolute())}")
        os.mkdir(dir_path)


    # Make Papermill Jupyter Notebooks
    for i, id_set in enumerate(id_sets):

        # Input Filename
        input_path = get_template_path()

        # Output Path
        report_title = report_titles[i]

        file_name = report_title \
            .translate(
                str.maketrans('', '', string.punctuation)
            ) \
            .lower() \
            .replace(" ", "_")

        output_path = pathlib.Path(f'{directory}/{file_name}.ipynb')

        # Parameters
        params = {
            'ids': id_set,
            'title': report_title,
            'data': data.to_json()
        }

        # Papermill Execute
        pm.execute_notebook(
            input_path  = input_path,
            output_path = output_path,
            parameters  = params,
            report_mode = True
        )

    #  >>>> NBCONVERT <<<< ----

    # Prep for Conversions

    # Convert to HTML

    # Convert to PDF

    pass 

# Test reporting.py version 2

