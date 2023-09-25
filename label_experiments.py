import hydra
import tqdm
from pathlib import Path

from raha.raha.labeler import Labeler

@hydra.main(version_base=None, config_path="hydra_configs", config_name="base")
def main(cfg):
    experiments_folder = Path(cfg["experiment"]["path_to_experiment"]).resolve()
    # get all possible states
    states = []
    for experiment in experiments_folder.iterdir():
        name = experiment.name
        experiment = experiment.joinpath(f"raha-baran-results-{name}")
        experiment = experiment.joinpath("state")
        for state in experiment.iterdir():
            print(state)
            states.append(state)

    start = cfg["execution"]["start"]
    if start < 0:
        start = 0

    end = cfg["execution"]["end"]
    if end is None or end > len(states):
        end = len(states)

    states = states[start:end]
    print(len(states))

    for state in tqdm.tqdm(states):
        print(state)
        labeler = Labeler()
        labeler.LABELING_BUDGET = cfg["raha"]["labeling_budget"]
        dd = labeler.load_state(state)
        labeler.VERBOSE = True
        detection_dictionary = labeler.run(dd)

        labeler.save_state(detection_dictionary, state.name)


if __name__ == '__main__':
    main()
