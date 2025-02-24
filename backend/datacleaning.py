import pandas as pd

df = pd.read_csv("../data.csv")

df["Date"] = pd.to_datetime(df["Date"])

df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour

df=df.drop(columns=['Branch'])