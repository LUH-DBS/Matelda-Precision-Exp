from pathlib import Path

import pandas as pd
from raha.predictor import Predictor

path_to_lake = Path("/home/malte/EDS-Baselines/experiments_2_lables_checked").resolve()

# states = []
for experiment in path_to_lake.iterdir():
    name = experiment.name
    experiment = experiment.joinpath(f"raha-baran-results-{name}")
    experiment = experiment.joinpath("state")
    if experiment.exists():
        for state in experiment.iterdir():
            predictor = Predictor()
            state = predictor.load_state(state)
            print(state.labeled_cells)

            df = pd.DataFrame(columns=["Dataset", "Row", "Column", "Value", "Ground Truth", "Label"])

            for key in state.labeled_cells:
                df.loc[len(df)] = {"Dataset": str(experiment.parent.parent),
                                   "Row": key[0],
                                   "Column": key[1],
                                   "Value": state.dataframe.iloc[key],
                                   "Ground Truth": state.labeled_cells[key][1],
                                   "Label": state.labeled_cells[key][0]}

            dataframe_path = experiment.parent.joinpath("labled_values.csv")
            df.to_csv(dataframe_path, index=False)

            # states.append(state)
