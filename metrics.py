import numpy as np

def calculate_metrics(initial, final, df, trades):
    # Basic performance
    profit = final - initial
    return_percent = (profit / initial) * 100 if initial != 0 else 0

    # Drawdown
    df['peak'] = df['equity'].cummax()
    df['drawdown'] = (df['equity'] - df['peak']) / df['peak']
    max_drawdown = df['drawdown'].min() * 100

    # Daily returns
    returns = df['equity'].pct_change().dropna()

    # Safe Sharpe ratio
    if len(returns) > 0 and returns.std() != 0:
        sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
    else:
        sharpe = 0

    # Trades analysis
    wins, losses = 0, 0
    profits = []

    for i in range(1, len(trades), 2):
        buy_price = trades[i-1][1]
        sell_price = trades[i][1]
        p = sell_price - buy_price
        profits.append(p)

        if p > 0:
            wins += 1
        else:
            losses += 1

    total_trades = wins + losses
    win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0

    gross_profit = sum(p for p in profits if p > 0)
    gross_loss = abs(sum(p for p in profits if p < 0))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0

    # 🔥 IMPORTANT: return dictionary
    return {
        "Initial Balance": initial,
        "Final Balance": final,
        "Profit": profit,
        "Return %": return_percent,
        "Max Drawdown %": max_drawdown,
        "Sharpe Ratio": sharpe,
        "Win Rate %": win_rate,
        "Profit Factor": profit_factor
    }