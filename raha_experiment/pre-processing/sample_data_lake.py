import logging

import hydra
import pandas as pd
import numpy as np
from pathlib import Path
import pickle

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="../hydra_configs", config_name="preprocessing")
def main(cfg):
    n_datasets = cfg["sampling"]["amount_of_datasets"]

    min_rows = cfg["sampling"]["minimum_rows"]
    max_rows = cfg["sampling"]["maximum_rows"]

    min_columns = cfg["sampling"]["minimum_columns"]
    max_columns = cfg["sampling"]["maximum_columns"]

    datalake_path = Path(cfg["sampling"]["datalake_path"]).resolve()

    if cfg["sampling"]["unidetect_training_corpus"] is not None:
        unidetect_trainings_set_path = Path(cfg["sampling"]["unidetect_training_corpus"]).resolve()
        with unidetect_trainings_set_path.open("rb") as file:
            trainings_set = pickle.load(file)
    else:
        trainings_set = []

    if not datalake_path.exists():
        exit()

    checkables = [datalake_path]
    paths = []

    while len(checkables) != 0:
        path = checkables.pop(0)
        for child in path.iterdir():
            if child.is_file():
                paths.append(child)
            elif child.is_dir():
                checkables.append(child)

    log.debug(f"Size of data lake: {len(paths)} files")
    log.info("Finished retrieving all file paths")

    datalake_index = pd.DataFrame(columns=["Path", "Rows", "Columns"])

    already_picked = []
    while datalake_index.shape[0] < n_datasets:
        index = np.random.randint(0, len(paths))
        csv_path = paths[index]
        log.info(f"chose {csv_path} as new path")
        if csv_path.is_dir():
            log.info("was dir")
            continue
        if str(csv_path) in trainings_set:
            log.info("was in trainings_set")
            continue

        log.debug("is file")
        df = pd.read_csv(csv_path)

        if min_rows <= df.shape[0] <= max_rows and min_columns <= df.shape[1] <= max_columns:
            if index not in already_picked:
                log.info("can be used")
                new_row = {'Path': csv_path, 'Rows': df.shape[0], 'Columns': df.shape[1]}
                datalake_index.loc[len(df)] = new_row
                already_picked.append(index)
            else:
                log.info("already used")
        else:
            log.info("too small or too tiny")

    datalake_index.to_csv(
        Path(cfg["sampling"]["sample_index"]).resolve(), index=False)


if __name__ == '__main__':
    main()
