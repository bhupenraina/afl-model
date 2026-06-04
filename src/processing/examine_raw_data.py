import pandas as pd

df = pd.read_csv("data/raw/data_fryzigg.csv")

# Number of rows
print(len(df))

# Column names
print(df.columns.tolist())