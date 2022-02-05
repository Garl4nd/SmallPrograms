import pandas as pd
import math
cf=pd.read_csv("Confirmed.csv")
print(type(cf))
names=[country if type(state) is not str else f"{state}/{country}" for state,country in zip(cf["Province/State"],cf["Country/Region"])]
print(names)
