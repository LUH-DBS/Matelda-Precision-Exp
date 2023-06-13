from pathlib import Path
import raha
from raha.raha.sampler import Sampler
import tqdm

path_to_experiments = Path("/home/malte/EDS-Baselines/experiments").resolve() # change here to change root repository for experiments
n_experiments = 1 # change here to run experiments n times -> generate n states with different tuples sampled

for experiment in tqdm.tqdm(path_to_experiments.iterdir()):
    
    if experiment.is_file():
        continue
    elif experiment.is_dir():
        for dataset in experiment.iterdir():
            if dataset.is_file() and dataset.suffix == ".csv":
                
                for i in range(n_experiments):
                    dataset_name = dataset.stem
                    dataset_dictionary = {
                            "name": dataset_name,
                            "path": dataset
                        }
                    sampler = Sampler()
                    detection_dictionary = sampler.run(dataset_dictionary)
                    sampler.save_state(detection_dictionary)
