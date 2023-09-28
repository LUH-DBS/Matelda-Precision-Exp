# EDS-Baselines
This repository contains code that performs the precision experiment of Raha and Uni-Detect on the real world 
data lake WDC for the paper Error Detection at Scale. Specifically, Raha needed to be adapted to allow streamlined user labeling, because no ground truth 
is available.
## Installation
1. Create a anaconda environment
   - use ``environment.yml`` or install packages manually. 
2. Install adapted raha
   - ``cd raha``
   - ``pip install -e .``
## Usage
There are multiple steps required to run the different experiments. The Raha precision experiment is 
executed in the following steps:
1. run ``python start_experiments.py``
2. After the script finished the sampled tuples need to be labeled. This can be done by running ``python label_experiments.py``. 
This requires user input!
   - Depending on the labeling budget this part can take a lot of time. Using the ``raha.start`` and ``raha.end`` in 
   the file ``hydra_configs/base.yaml`` the work can be split into different sessions. 
   - If needed the execution can be stopped by using ``Strg+C``. Remember to set the ``raha.start`` in 
   the file ``hydra_configs/base.yaml``
   - Same value entered means correct, any other value means error
3. The last step uses the labels to execute the prediction part of Raha. This can be done by running ``python finish_experiments.py``
   - ``raha.start`` and ``raha.end`` in the file ``hydra_configs/base.yaml`` also control the execution here.