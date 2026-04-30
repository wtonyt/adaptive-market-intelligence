import pandas as pd
import os

def load_silver():
    return pd.read_parquet("data/silver/market_data_clean.parquet")

def create_features(df):
    df = df.copy()

    # Sort properly
    df = df.sort_values(["symbol", "date"])

    # Daily return
    df["return"] = df.groupby("symbol")["close"].pct_change()

    # Moving averages
    df["ma_5"] = df.groupby("symbol")["close"].transform(lambda x: x.rolling(5).mean())
    df["ma_10"] = df.groupby("symbol")["close"].transform(lambda x: x.rolling(10).mean())

    # Volatility (rolling std)
    df["volatility_5"] = df.groupby("symbol")["return"].transform(lambda x: x.rolling(5).std())

    return df

def create_target(df):
    df = df.copy()

    # Next day return
    df["next_return"] = df.groupby("symbol")["return"].shift(-1)

    # Classification target
    df["target"] = (df["next_return"] > 0).astype(int)

    return df

def save_gold(df):
    os.makedirs("data/gold", exist_ok=True)
    df.to_parquet("data/gold/market_features.parquet", index=False)
    print("Saved gold layer")

if __name__ == "__main__":
    df = load_silver()
    df = create_features(df)
    df = create_target(df)
    df = df.dropna()
    save_gold(df)
