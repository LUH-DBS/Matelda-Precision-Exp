from pathlib import Path
import raha
from raha.raha.predictor import Predictor
from raha.raha.sampler import Sampler
import tqdm
import argparse
import tqdm
from pathlib import Path

path_to_experiments = Path("/home/malte/EDS-Baselines/experiments").resolve() # change here to change root repository for experiments
n_experiments = 1 # change here to run experiments n times -> generate n states with different tuples sampled

parser = argparse.ArgumentParser()
parser.add_argument('--start', help='Integer at which experiment to start labeling', type=int,default=0)
parser.add_argument('--end', help='Integer at which experiment to end labeling', type=int)
args = parser.parse_args()

experiments_folder = Path("./experiments").resolve()

#get all possible states
states = []
for experiment in experiments_folder.iterdir():
    name = experiment.name
    experiment = experiment.joinpath(f"raha-baran-results-{name}")
    experiment = experiment.joinpath("state")
    if experiment.exists():
        for state in experiment.iterdir():

            print(state)
            states.append(state)
end = args.end
if end is None or end > len(states):
    end = len(states)
states = states[args.start:end]
print(len(states))

for state in states:
    predictor = Predictor()
    predictor.LABELING_BUDGET = 1
    dd = predictor.load_state(state)
    d = predictor.run(dd)
    predictor.save_state(d, state.name)
