import logging

import hydra
import pandas as pd
from pathlib import Path

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="../hydra_configs", config_name="preprocessing")
def main(cfg):
    df = pd.read_csv(Path(cfg["sampling"]["sample_index"]).resolve())
    wd = Path(cfg["experiment"]["path_to_experiment"]).resolve()

    wd.mkdir(exist_ok=True)

    log.info(f"Copy experiment datasets to {wd}")

    for index, row in df.iterrows():
        path = Path(row["Path"]).resolve()
        tmp_df = pd.read_csv(path)
        tmp_path = wd.joinpath(path.stem)
        tmp_path.mkdir(exist_ok=True)
        tmp_path = tmp_path.joinpath(path.name)
        tmp_df.to_csv(tmp_path, index=False)
        log.info(f"Copied {str(path)} to {str(tmp_path)}")


if __name__ == '__main__':
    main()
