# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 10 (Jupyter Automated Reporting, Part 2): NBConvert HTML & PDF ----

# IMPORTS ----

import glob
import pathlib
from tqdm import tqdm

from traitlets.config import Config
from nbconvert.preprocessors import TagRemovePreprocessor
from nbconvert.exporters import HTMLExporter, PDFExporter
from nbconvert.writers import FilesWriter


# 1.0 NBCONVERT CONFIG ----

# Configure our tag removal
# - https://nbconvert.readthedocs.io/en/latest/removing_cells.html

c = Config()

c.TemplateExporter.exclude_input = True
c.TagRemovePreprocessor.remove_cell_tags = ("remove_cell",)
c.TagRemovePreprocessor.remove_all_outputs_tags = ("remove_output",)
c.TagRemovePreprocessor.remove_input_tags = ('remove_input',)
c.TagRemovePreprocessor.enabled = True

c

# GET FILE LIST ----

# Get file list for conversion

files = glob.glob('09_jupyter_papermill/reports/sales_forecast*.ipynb')

files

file_path = pathlib.Path(files[0])

file_path.stem
file_path.name
file_path.parents[0]

# 2.0 HTML EXPORT ----

c.HTMLExporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor"]
c

(body, resources) = HTMLExporter(config = c) \
    .from_filename(file_path)

file_dir      = file_path.parents[0]
file_dir_html = str(file_dir) + "_html"

c.FilesWriter.build_directory = str(file_dir_html)
c

fw = FilesWriter(config = c)
fw

fw.write(body, resources, notebook_name="test")

# Iterate through files ----

for file in tqdm(files):
    
    file_path = pathlib.Path(file)
    file_name = file_path.stem
    file_dir  = file_path.parents[0]

    (body, resources) = HTMLExporter(config = c).from_filename(file_path)
    file_dir_html = str(file_dir) + "_html"
    c.FilesWriter.build_directory = str(file_dir_html)
    fw = FilesWriter(config = c)
    fw.write(body, resources, notebook_name=file_name)




# 3.0 PDF EXPORT ----
# - REQUIRES MIKETEX: https://miktex.org/download
# Stack Overflow: https://stackoverflow.com/questions/59225719/latex-error-related-to-tcolorbox-sty-not-found


for file in tqdm(files):

    file_path = pathlib.Path(file)
    file_name = file_path.stem
    file_dir  = file_path.parents[0]

    (body, resources) = PDFExporter(config=c).from_filename(file_path)
    file_dir_pdf = str(file_dir) + "_pdf"
    c.FilesWriter.build_directory = str(file_dir_pdf)
    fw = FilesWriter(config = c)
    fw.write(body, resources, notebook_name=file_name)
