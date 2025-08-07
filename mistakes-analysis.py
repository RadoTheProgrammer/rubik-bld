import pandas as pd
from pandas import Timestamp
now = pd.Timestamp.now()
print(repr(now))
df = pd.read_csv("data-all.csv")
dfd = {col:[] for col in ("Number","Avg","Avg5")}
indexes = ["PlanMistake","MemoMistake","DoMistake"]
for index in indexes:
    series = df[index].dropna()
    dfd["Number"].append(len(series))
    dfd["Avg"].append(series.mean())
    series5 = series.iloc[-5:]
    #print(series5)
    dfd["Avg5"].append(series5.mean())

df_output = pd.DataFrame(dfd)
print(df_output)

