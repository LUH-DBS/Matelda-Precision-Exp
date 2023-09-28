import logging
from pathlib import Path

import hydra

from raha.sampler import Sampler
import tqdm

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="hydra_configs", config_name="base")
def main(cfg):
    path_to_experiments = Path(cfg["experiment"]["path_to_experiment"]).resolve()
    n_experiments = cfg["experiment"]["n_experiments"]
    for experiment in tqdm.tqdm(list(path_to_experiments.iterdir())):

        if experiment.is_file():
            continue
        elif experiment.is_dir():
            for dataset in experiment.iterdir():
                if dataset.is_file() and dataset.suffix == ".csv":

                    for i in range(n_experiments):
                        dataset_name = dataset.stem
                        dataset_dictionary = {
                            "name": dataset_name,
                            "path": dataset
                        }
                        sampler = Sampler()
                        sampler.LABELING_BUDGET = cfg["raha"]["labeling_budget"]
                        detection_dictionary = sampler.run(dataset_dictionary)
                        sampler.save_state(detection_dictionary)


if __name__ == '__main__':
    main()
