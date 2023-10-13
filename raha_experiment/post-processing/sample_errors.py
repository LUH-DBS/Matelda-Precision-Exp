import logging
from pathlib import Path

import hydra
import pandas as pd

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="../hydra_configs", config_name="postprocessing")
def main(cfg):
    path_to_errors = Path(cfg["retrival"]["error_index_path"]).resolve()
    df = pd.read_csv(path_to_errors)

    log.info(f"Before excluding non-classifier errors{df.shape}")
    df = df[df["Probability"] > 0]
    log.info(f"After excluding non-classifier errors{df.shape}")

    choices = df.sample(cfg["sampling"]["n_samples"])
    log.info(choices)

    choices.to_csv(Path(cfg["sampling"]["path_to_error_samples"]).resolve(), index=False)


if __name__ == '__main__':
    main()
