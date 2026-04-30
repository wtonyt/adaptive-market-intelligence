import pandas as pd
import os


def load_bronze():
    return pd.read_parquet("data/bronze/market_data.parquet")


def clean_data(df):
    # Make a clean copy
    df = df.dropna().copy()

    # Standardize column names
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]

    # Convert numeric columns
    numeric_cols = ["open", "high", "low", "close", "adj_close", "volume"]

    for col in numeric_cols:
        if col in df.columns:
            df.loc[:, col] = pd.to_numeric(df[col], errors="coerce")

    # Convert date column
    if "date" in df.columns:
        df.loc[:, "date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop rows that failed conversion
    df = df.dropna()

    # Sort for consistency
    if "symbol" in df.columns and "date" in df.columns:
        df = df.sort_values(["symbol", "date"])

    return df


def save_silver(df):
    os.makedirs("data/silver", exist_ok=True)
    df.to_parquet("data/silver/market_data_clean.parquet", index=False)
    print("Saved silver layer")


if __name__ == "__main__":
    df = load_bronze()
    df_clean = clean_data(df)
    save_silver(df_clean)
