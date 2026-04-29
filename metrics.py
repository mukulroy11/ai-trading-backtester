def calculate_metrics(initial, final, df):
    profit = final - initial
    return_percent = (profit / initial) * 100

    # Drawdown
    df['peak'] = df['equity'].cummax()
    df['drawdown'] = (df['equity'] - df['peak']) / df['peak']

    max_drawdown = df['drawdown'].min() * 100

    return {
        "Initial Balance": initial,
        "Final Balance": final,
        "Profit": profit,
        "Return %": return_percent,
        "Max Drawdown %": max_drawdown
    }