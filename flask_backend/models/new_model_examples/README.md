# New self-created model dockerization
Congratulations, you've got a great set of data and would like to make a model, dockerize it, and perhaps share with the broader PredictMod ecosystem. 

## Here, we provide an example template that performs all of these steps. 
Feel free to mix up steps, this tutorial is by no means prescriptive - merely a guide to demonstrate the barebones basics of creating a model with a data set, saving it, and using PredictMod-provided scripts to create a docker container hosted within the PredictMod platform.

## Getting started
All of the requirements for running PredictMod from the [main documentation](https://github.com/GW-HIVE/PredictMod/blob/main/README.md) with `docker` apply here. 

## Creating a model
If you have data to work with, feel free to try using that. We have also provided a dummy data generator that quickly creates a training set, and an example selected from it, in `random_daata.py`. It is designed to provide a very easily-classified data set, strictly for pedagogical purposes within this tutorial.

### Create data, if needed
Run `random_data.py` to generate ~10 MB of training data and a sample taken from the same. Files will be named `example_feature_data.csv` and `example_sample_point.csv`. 

### Train a model
Run the `example_classifier.py` script to train a model (by default, a Decision Tree Classifier from `scikit-learn`) and save it to a python "pickle" (`.pkl`) file. 

### Run the model
Run the `example_predictor.py` script to load the model and sample data point to generate a prediction.

### Explore the metadata
By default, there is a BCO template to be filled in, with all fields available for editing in your favorite text editor. There is also a `model_metadata.py` script that will provide some basic introspection into the resulting model, when the docker is run within the PredictMod framework.

## Building the docker
Navigate to the scripts directory (`PredictMod/scripts`) and edit `build_backends.py:10` and `run_backends.py:16` to read `IS_EXAMPLE = True`.
Running `python3 build_backends.py` and `python3 run_backends.py` should now:  
1 - Build an appropriate docker container  
2 - Mount the countainer to both the data-loading directory and the local PredictMod docker network  
3 - Host your new model within a self-contained docker container  

