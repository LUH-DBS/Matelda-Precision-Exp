import logging

import hydra
from raha.predictor import Predictor

import tqdm
from pathlib import Path

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="hydra_configs", config_name="base")
def main(cfg):
    experiments_folder = Path(cfg["experiment"]["path_to_experiment"]).resolve()
    # get all possible states
    states = []
    for experiment in experiments_folder.iterdir():
        name = experiment.name
        experiment = experiment.joinpath(f"raha-baran-results-{name}")
        experiment = experiment.joinpath("state")
        if experiment.exists():
            for state in experiment.iterdir():
                log.debug(state)
                states.append(state)

    start = cfg["execution"]["start"]
    if start < 0:
        start = 0

    end = cfg["execution"]["end"]
    if end is None or end > len(states):
        end = len(states)

    states = states[start:end]
    log.info(f"Datasets to finish: {len(states)}")

    for state in tqdm.tqdm(states):
        predictor = Predictor()
        predictor.LABELING_BUDGET = cfg["raha"]["labeling_budget"]
        dd = predictor.load_state(state)
        d = predictor.run(dd)
        predictor.save_state(d, state.name)


if __name__ == '__main__':
    main()
