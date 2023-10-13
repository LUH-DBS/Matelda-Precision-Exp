import logging
from pathlib import Path

import hydra
import pandas as pd
from raha.predictor import Predictor

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="../hydra_configs", config_name="postprocessing")
def main(cfg):
    path_to_lake = Path(cfg["experiment"]["path_to_experiment"]).resolve()

    # states = []
    for experiment in path_to_lake.iterdir():
        name = experiment.name
        experiment = experiment.joinpath(f"raha-baran-results-{name}")
        experiment = experiment.joinpath("state")
        if experiment.exists():
            for state in experiment.iterdir():
                predictor = Predictor()
                state = predictor.load_state(state)
                log.debug(state.labeled_cells)

                df = pd.DataFrame(columns=["Dataset", "Row", "Column", "Value", "Ground Truth", "Label"])

                for key in state.labeled_cells:
                    df.loc[len(df)] = {"Dataset": str(experiment.parent.parent),
                                       "Row": key[0],
                                       "Column": key[1],
                                       "Value": state.dataframe.iloc[key],
                                       "Ground Truth": state.labeled_cells[key][1],
                                       "Label": state.labeled_cells[key][0]}

                dataframe_path = experiment.parent.joinpath("labeled_values.csv")
                df.to_csv(dataframe_path, index=False)

                # states.append(state)


if __name__ == '__main__':
    main()
