def run_backtest(df, initial_balance=10000):
    balance = initial_balance
    position = 0

    trades = []
    equity_curve = []

    for i in range(len(df)):
        price = df['Close'].iloc[i]

        # Buy
        if df['buy_signal'].iloc[i] and position == 0:
            position = balance / price
            balance = 0
            trades.append(("BUY", price))

        # Sell
        elif df['sell_signal'].iloc[i] and position > 0:
            balance = position * price
            position = 0
            trades.append(("SELL", price))

        # Track equity
        current_value = balance if position == 0 else position * price
        equity_curve.append(current_value)

    final_value = equity_curve[-1]

    df['equity'] = equity_curve

    return final_value, trades, df