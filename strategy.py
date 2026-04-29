import ta

def apply_strategy(df):
    close = df['Close'].squeeze()

    df['rsi'] = ta.momentum.RSIIndicator(close, window=14).rsi()

    df['buy_signal'] = df['rsi'] < 30
    df['sell_signal'] = df['rsi'] > 70

    return df