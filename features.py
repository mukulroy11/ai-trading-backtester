import ta

def create_features(df):
    close = df['Close'].squeeze()

    df['rsi'] = ta.momentum.RSIIndicator(close, window=14).rsi()
    df['macd'] = ta.trend.MACD(close).macd()
    df['ema'] = ta.trend.EMAIndicator(close, window=20).ema_indicator()

    df.dropna(inplace=True)

    df['target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    return df