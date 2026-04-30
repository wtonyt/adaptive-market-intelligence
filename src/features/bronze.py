import pandas as pd
import glob
import os

def load_raw_data():
    files = glob.glob("data/raw/*/*.csv")
    dfs = []

    for file in files:
        df = pd.read_csv(file)
        symbol = file.split("/")[-2]
        df["symbol"] = symbol
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

def save_bronze(df):
    os.makedirs("data/bronze", exist_ok=True)
    df.to_parquet("data/bronze/market_data.parquet", index=False)
    print("Saved bronze layer")

if __name__ == "__main__":
    df = load_raw_data()
    save_bronze(df)
