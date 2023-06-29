from pathlib import Path

import numpy as np
import pandas as pd

from raha.raha.predictor import Predictor


experiments_folder = Path("X:\\Projekte\\EDS-Baselines\\raha\\datasets").resolve()
n_samples = 100

#get all possible states
detected_errors = []
for experiment in experiments_folder.iterdir():
    name = experiment.name
    dataset_path = experiment
    experiment = experiment.joinpath(f"raha-baran-results-{name}")
    experiment = experiment.joinpath("state")
    if not experiment.exists():
        continue
    for state in experiment.iterdir():

        #print(state)
        loader = Predictor()
        d = loader.load_state(state)
        #print(d.detected_cells)
        error = [(dataset_path, state, item, d.detected_cells[item]) for item in d.detected_cells.keys()]
        error = list(filter(lambda x: x[3] != 'JUST A DUMMY VALUE', error))
        detected_errors += error

df = pd.DataFrame(columns=["Value", "Ground Truth", "IsError", "Probability", "Row", "Column",  "Dataset", "State", ])
detected_errors = sorted(detected_errors, key=lambda x: x[3])

choices = detected_errors[len(detected_errors) - n_samples:]

for tup in choices:
    error = tup
    loader = Predictor()
    d = loader.load_state(error[1])
    row = {'Value': d.dataframe.iloc[error[2]],
           'Ground Truth': "",
           'IsError': "",
           'Probability': error[3],
           'Row': error[2][0],
           'Column': error[2][1],
           'Dataset': error[0],
           'State': error[1]}
    df.loc[len(df)] = row

print(df)
df = df.sort_values("Dataset")
df.to_csv(experiments_folder.joinpath("sampled_errors.csv").resolve(), index=False)
