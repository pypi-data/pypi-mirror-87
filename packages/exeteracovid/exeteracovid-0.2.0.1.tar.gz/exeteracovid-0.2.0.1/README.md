# ExeTeraCovid

Welcome to the ExeTeraCovid Readme!

Current Release v0.2.0.1

This page and the accompanying wiki show you how to use [ExeTera](https://github.com/KCL-BMEIS/ExeTera.git) to create reproducible analysis pipelines for the Covid Symptom Study dataset.

This project contains a set of notebooks, scripts and algorithms to help you analyse and write new analyses for the Covid Symptom Study data.
ExeTera is a software developed by King's College London to provide data curation for the Covid Symptom Study dataset. The dataset is collected using the Covid Symptom Study app, developed by Zoe Global Ltd with input from King's College London, the Massachusetts General Hospital, Lund University Sweden, and Uppsala University, Sweden.
This project contains the following:
* **Notebooks**: Python notebooks containing ready to run analyses
* **Scripts**: Python scripts containing ready to run analyses
* **Algorithms**: A number of useful algorithms for cleaning / processing of Covid Symptom Study data, to be used in your own scripts
* **Processing**: A number of useful pieces of functionality, to be used in your own scripts

# Running analyses

Running analyses is a simple process:
1. Fetch the dataset snapshot(s)
1. Import the dataset, using `exetera import`
1. Run the postprocessing script on the imported dataset, either via notebook or script
1. Run analytics!

## Fetch the dataset snapshot(s)
The Covid Symptom Study is delivered as a series of daily csv snapshots. If you do not otherwise have access to the snapshots as a research institution, you can get them from [The Health Data Gateway](https://web.www.healthdatagateway.org/dataset/fddcb382-3051-4394-8436-b92295f14259).

## Import the dataset
Importing the dataset requires the following:
 * The data snapshots
 * The schema file for the dataset `covid_schema.json` which can be found in this project
 * ExeTera, which can be installed using the command `pip install ExeTera`

```
exetera import
-s path/to/covid_schema.json \
-i "patients:path/to/patient_data.csv, assessments:path/to/assessmentdata.csv, tests:path/to/covid_test_data.csv, diet:path/to/diet_study_data.csv" \
-o path/to/output_dataset_name.hdf5
```

## Run the postprocessing script on the imported dataset
This can be done one of two ways:
* Via python notebook using `exeteracovid/notebooks/standard_processing.ipynb`
* Via python script using `exeteracovid/scripts/standard_processing.py`

### Via python notebook
Fill in the fields for `input_filename` and `output_filename`, and then run the cell

### Via python script

```
standard_processing -i path/to/input_dataset -o path/to/output_dataset -d
```
#### Arguments
 * `-i/--input`: The path and name of the import hdf5 file
 * `-o/--output`: The path and name of the processed hdf5 file
 * `-d/--daily`: A flag to indicate whether to generate daily assessments (optional)

### Government Open Licence v3.0 attribution statement
The resources folder contains, amongst other resources, CSV files containing lsoa11cd geo-data that are required for certain scripts and are derived from data sources made available by [https://data.gov.uk](https://data.gov.uk). These sources are used in accordance with the [Open Government Licence V3.0](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)
