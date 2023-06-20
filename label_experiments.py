import argparse
import tqdm
from pathlib import Path

from raha.raha.labeler import Labeler

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
    for state in experiment.iterdir():

        print(state)
        states.append(state)
end = args.end
if end is None or end > len(states):
    end = len(states)
states = states[args.start:end]
print(len(states))

for state in tqdm.tqdm(states):
        print(state)
        labeler = Labeler()
        labeler.LABELING_BUDGET = 1
        dd = labeler.load_state(state)
        labeler.VERBOSE = True
        detection_dictionary = labeler.run(dd)

        labeler.save_state(detection_dictionary, state.name)
