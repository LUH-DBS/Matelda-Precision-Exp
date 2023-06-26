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
        detected_errors += [(dataset_path, state, item) for item in d.detected_cells.keys()]

df = pd.DataFrame(columns=["Value", "IsError", "Row", "Column",  "Dataset", "State", ])

choices = np.random.choice(np.arange(len(detected_errors)), n_samples, replace=False)
print(choices)
for index in choices:
    error = detected_errors[index]
    loader = Predictor()
    d = loader.load_state(error[1])
    row = {'Value': d.dataframe.iloc[error[2]],
           'IsError': "",
           'Row': error[2][0],
           'Column': error[2][1],
           'Dataset': error[0],
           'State': error[1]}
    df.loc[len(df)] = row

print(df)
df = df.sort_values("Dataset")
df.to_csv(experiments_folder.joinpath("sampled_errors.csv").resolve(), index=False)