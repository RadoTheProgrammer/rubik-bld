import pandas as pd
from pandas import Timestamp
now = pd.Timestamp.now()
print(repr(now))
df = pd.read_csv("data_single.csv")
print(df["PlanMistake"].sum())
print(df["MemoTime"].sum())