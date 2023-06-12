import pandas as pd
import numpy as np
from pathlib import Path

n_datasets = 100

min_rows = 21
max_rows = 100000

min_columns = 3
max_columns = 10

datalake_path = Path("/home/fatemeh/EDS-Datasets/WDC_Corpus/scsv").resolve()
print(datalake_path)

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

print(len(paths))
print("Finished retrieving all file paths")


datalake_index = pd.DataFrame(columns=["Path"])

while datalake_index.shape[0] < n_datasets:
    index = np.random.randint(0, len(paths))
    csv_path = paths[index]
    print(f"chose {csv_path} as new path")
    if csv_path.is_dir():
        print("was dir")
        continue
    print("is file")
    df = pd.read_csv(csv_path)

    if min_rows <= df.shape[0] <= max_rows and min_columns <= df.shape[1] <= max_columns:
        print("can be used")
        new_row = {'Path': csv_path, 'Rows': df.shape[0], 'Columns': df.shape[1]}
        datalake_index.loc[len(df)] = new_row

datalake_index.to_csv(Path("/home/malte/EDS-Baselines/datalake_index.csv").resolve())
