from pathlib import Path
import raha
from raha.raha.predictor import Predictor
from raha.raha.sampler import Sampler
import tqdm

path_to_experiments = Path("/home/malte/EDS-Baselines/experiments").resolve() # change here to change root repository for experiments
n_experiments = 1 # change here to run experiments n times -> generate n states with different tuples sampled

for experiment in tqdm.tqdm(path_to_experiments.iterdir()):
    
    if experiment.is_file():
        continue
    elif experiment.is_dir():
        for file in experiment.iterdir():
            if file.is_dir():
                state_path = file.joinpath("state")
                for state in state_path.iterdir():
                        predictor = Predictor()
                        predictor.LABELING_BUDGET = 1
                        dd = predictor.load_state(state)
                        d = predictor.run(dd)
                        predictor.save_state(d, state.name)
