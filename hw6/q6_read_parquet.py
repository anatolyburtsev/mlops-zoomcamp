import pandas as pd

df = pd.read_parquet("./output_file.parquet")

print(df.head())