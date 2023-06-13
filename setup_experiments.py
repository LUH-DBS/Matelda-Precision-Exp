import pandas as pd
from pathlib import Path



df = pd.read_csv(Path("/home/malte/EDS-Baselines/datalake_index.csv").resolve())
wd = Path.cwd().joinpath("experiments")
wd.mkdir(exist_ok=True)

print(f"Move experiment datasets to {wd}")

for index,row in df.iterrows():
    path = Path(row["Path"]).resolve()
    tmp_df = pd.read_csv(path)
    tmp_path = wd.joinpath(path.stem)
    tmp_path.mkdir(exist_ok=True)
    tmp_path = tmp_path.joinpath(path.name)
    tmp_df.to_csv(tmp_path, index=False)

    
