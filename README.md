# EDS-Baselines
This repository contains code that performs the precision experiment of Raha and Uni-Detect on the real world 
data lake WDC.

Specifically, Raha needed to be adapted to allow streamlined user labeling, because no ground truth 
is available. For this Raha was split into three different scripts, allowing the user to do all required user input in 
one concentrated step in the experiment. This allows unsupervised execution of the rest of raha.
## Installation
1. Create an anaconda environment
   - use ``environment.yml`` or install packages manually. 
2. Install adapted raha
   - ``cd raha``
   - ``pip install -e .``
## Usage
There are multiple steps required to run the different experiments. The Raha precision experiment is 
executed in the following steps:
1. Configure the configs in ``raha_experiment/hydra_configs``
2. Setup the experimental data
   - download WDC data lake and convert to csv files
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