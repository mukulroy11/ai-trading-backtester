import yfinance as yf
import pandas as pd

def load_data(symbol="AAPL", start="2020-01-01", end="2023-01-01"):
    df = yf.download(symbol, start=start, end=end)

    # Fix multi-index issue
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Force Close column to 1D
    df['Close'] = df['Close'].squeeze()

    df.dropna(inplace=True)

    return df