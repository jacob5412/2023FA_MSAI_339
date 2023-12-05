# Instructions

The notebooks are ordered in the following way:
1. [NYC_Taxi_EDA](NYC_Taxi_EDA.ipynb): Contains the Exploratory Data Analysis
2. [NYC_Taxi_Model_Selection](NYC_Taxi_Model_Selection.ipynb): Contains some basic modelling with a simple gridsearch
3. [NYC_Taxi_Pipeline](NYC_Taxi_Pipeline.ipynb): Contains the pipeline use for preprocessing data and a random forest model making inferences using the best hyperparameters.

**Miscellaneous**:
* Logs can be found in `/mlruns`
* Data is to be stored in `/data`
* If you would like to run your own OSRM service, follow the instructions listed in `OSRM.md`
* `preprocessing_utils.py` contains the preprocessing classes for the pipeline
