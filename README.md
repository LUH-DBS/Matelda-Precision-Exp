# EDS-Baselines Precision Experiments
This repository contains code that performs the precision experiment of Raha on data lakes with no ground truth. 
Specifically, Raha needed to be adapted to allow efficient experiment execution by grouping all user labeling into one step.

## Installation
1. Create an anaconda environment
   - use ``environment.yml``
2. Install adapted raha
   - ``` shell
     cd raha
     pip install -e .
     cd ..
## Usage
There are multiple steps required to run the different experiments. The Raha precision experiment is 
executed in the following steps:
1. Configure the configs in ``raha_experiment/hydra_configs``
2. Setup the experimental data
   - prepare a data lake (for example the WDC data lake) in a folder (every dataset needs to be in csv format)
   - sample datasets from the data lake with ``python raha_experiment/pre-processing/sample_data_lake.py``
   - Using ``python raha_experiment/pre-processing/setup_experiments.py`` the folder structure necessary for Raha 
   can be created
3. run ``python raha_experiment/start_experiments.py``
4. After the script finished the sampled tuples need to be labeled. This can be done 
by running ``python raha_experiment/label_experiments.py``. 
This requires user input and can take a lot of time!
   - Depending on the labeling budget this part can take a lot of time. Using the ``raha.start`` and ``raha.end`` in 
   the file ``raha_experiment/hydra_configs/base.yaml`` the work can be split into different sessions. 
   - If needed the execution can be stopped by using ``Strg+C``. Remember to set the ``raha.start`` in 
   the file ``raha_experiment/hydra_configs/base.yaml``
   - Same value entered means correct, any other value means error
5. The last step uses the labels to execute the prediction part of Raha. This can be done 
by running ``python raha_experiment/finish_experiments.py``
   - ``raha.start`` and ``raha.end`` in the file ``raha_experiment/hydra_configs/base.yaml`` also control the execution here.
6. The results of Raha can then further be used by:
   - ``python raha_experiment/post-processing/retrieve_detected_errors.py``: to collect all detected errors into one csv
   - ``python raha_experiment/post-processing/sample_errors.py``: to sample an amount of errors from the csv that contains all errors
   - ``python raha_experiment/post-processing/retrieve_labels.py``: to collect all user labels to allow others to see 
   what has been labeled (to ensure consistency)
## Experiment

The configs are configured for the experiment run in the paper. Only the config at 
``raha_experiment/hydra_configs/preprocessing.yaml`` needs to be changed as it is configured for the test_lake.

Changes:
   - ``sampling.maximum_columns``: ``20`` -> ``10``
   - ``sampling.amount_of_datasets``: ``1`` -> ``100``
   - ``sampling.unidetect_training_corpus``: ``null`` -> a pickled list of paths pointing to datasets in the lake, 
   that have been used for training unidetect or should in general be excluded
   - ``sampling.datalake_path``: ``./test_lake`` -> path pointing towards the WDC lake
