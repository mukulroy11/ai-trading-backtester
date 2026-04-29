def train_model(df):
    # No heavy ML model (safe for Windows restrictions)
    return None


def generate_signals(df, model=None):
    # Simple AI-like logic using indicators

    df['buy_signal'] = (df['rsi'] < 30) & (df['macd'] > 0)
    df['sell_signal'] = (df['rsi'] > 70) & (df['macd'] < 0)

    return df