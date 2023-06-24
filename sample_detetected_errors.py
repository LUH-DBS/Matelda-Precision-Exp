from pathlib import Path

from raha.raha.predictor import Predictor


experiments_folder = Path("./experiments").resolve()

#get all possible states
detected_errors = []
for experiment in experiments_folder.iterdir():
    name = experiment.name
    experiment = experiment.joinpath(f"raha-baran-results-{name}")
    experiment = experiment.joinpath("state")
    for state in experiment.iterdir():

        print(state)
        loader = Predictor()
        d = loader.load_state(state)
        print(d.detected_cells)
        detected_errors.append(state)

print(len(detected_errors))