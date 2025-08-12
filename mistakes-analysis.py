MISTAKE_NAME = "MemoMistake"
import rrstats

import pandas as pd
from pandas import Timestamp
now = pd.Timestamp.now()

df = pd.read_csv("my-data.csv")
df = df.loc[df[MISTAKE_NAME].notna()][["Datetime",MISTAKE_NAME]]
print(df)
print(f"Mean: {df[MISTAKE_NAME].mean()}")
print(f"Mean of 5: {df[MISTAKE_NAME][-5:].mean()}")
#print(rrstats.StatsSeries(df["PlanMistake"]).myrolling(5).mean())
