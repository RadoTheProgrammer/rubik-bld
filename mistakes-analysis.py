MODE="MEMO"

import rrstats

import pandas as pd
from pandas import Timestamp
now = pd.Timestamp.now()

if MODE=="PLAN":
    MISTAKE_NAME = "PlanMistake"
    OTHER_COLS = ["PlanTime"]

elif MODE=="MEMO":
    MISTAKE_NAME = "MemoMistake"
    OTHER_COLS = ["MemoTime","MemoRecallTime","MemoEndTime"]

elif MODE=="DO":
    MISTAKE_NAME = "DoMistake"
    OTHER_COLS = ["DoTime"]
df = pd.read_csv("my-data.csv")
df = df.loc[df[MISTAKE_NAME].notna()][["Datetime",MISTAKE_NAME]+OTHER_COLS]
df["mean5"] = rrstats.StatsSeries(df[MISTAKE_NAME]).myrolling(5).mean()

print(df)
print(f"Mean: {df[MISTAKE_NAME].mean()}")
