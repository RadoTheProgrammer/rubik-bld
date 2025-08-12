import pandas as pd

df = pd.DataFrame({"a":["àé"]})
print(df.to_csv("sandbox.csv"))
