from pathlib import Path

import pandas as pd

sampled_errors = Path("X:\\Projekte\\EDS-Baselines\\raha\\datasets\\sampled_errors.csv").resolve()

df = pd.read_csv(sampled_errors)
precision = df["IsError"].sum()/len(df)
print(f"Precision: {precision}")
