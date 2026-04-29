import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from data_loader import load_data
from features import create_features
from ai_model import train_model, generate_signals
from strategy import apply_strategy
from backtester import run_backtest
from metrics import calculate_metrics

# Page config
st.set_page_config(page_title="Trading AI Platform", layout="wide")

# Dark theme styling
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
[data-testid="stSidebar"] { background-color: #111827; }
.stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 AI Trading Backtesting Dashboard")

# Sidebar
st.sidebar.header("⚙️ Configuration")

symbol = st.sidebar.text_input("Symbol", "AAPL")
strategy_type = st.sidebar.selectbox("Strategy", ["Rule-Based", "AI-Based"])
initial_balance = st.sidebar.number_input("Initial Balance", value=10000)

run = st.sidebar.button("Run Backtest")

# ================= MAIN LOGIC =================
if run:
    st.write("Fetching data...")
    df = load_data(symbol)

    # Apply strategy
    if strategy_type == "AI-Based":
        df = create_features(df)
        model = train_model(df)
        df = generate_signals(df, model)
    else:
        df = apply_strategy(df)

    # Run backtest
    final_value, trades, df = run_backtest(df, initial_balance)
    results = calculate_metrics(initial_balance, final_value, df)

    # ================= METRICS =================
    st.subheader("📊 Performance")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Initial", f"${results['Initial Balance']:.2f}")
    col2.metric("Final", f"${results['Final Balance']:.2f}")
    col3.metric("Return %", f"{results['Return %']:.2f}%")
    col4.metric("Drawdown", f"{results['Max Drawdown %']:.2f}%")

    # ================= CANDLESTICK =================
    st.subheader("🕯️ Candlestick Chart")

    fig_candle = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])

    fig_candle.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig_candle, width='stretch')

    # ================= EQUITY CURVE =================
    st.subheader("📈 Equity Curve")

    fig_equity = go.Figure()

    fig_equity.add_trace(go.Scatter(
        x=df.index,
        y=df['equity'],
        mode='lines',
        name='Equity'
    ))

    fig_equity.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(fig_equity, width='stretch')

    # ================= DRAWDOWN =================
    st.subheader("📉 Drawdown")

    fig_dd = go.Figure()

    fig_dd.add_trace(go.Scatter(
        x=df.index,
        y=df['drawdown'],
        fill='tozeroy',
        name='Drawdown'
    ))

    fig_dd.update_layout(
        template="plotly_dark",
        height=300
    )

    st.plotly_chart(fig_dd, width='stretch')

    # ================= PRICE LINE =================
    st.subheader("📊 Price Line")

    fig_line, ax = plt.subplots()
    ax.plot(df['Close'], linewidth=1.5)
    ax.set_facecolor("#0e1117")
    fig_line.patch.set_facecolor("#0e1117")
    ax.tick_params(colors='white')
    ax.set_title(symbol, color="white")

    st.pyplot(fig_line)

    # ================= SIGNALS =================
    st.subheader("📍 Buy / Sell Signals")

    fig_sig, ax_sig = plt.subplots()
    ax_sig.plot(df['Close'])

    buy = df[df['buy_signal']]
    sell = df[df['sell_signal']]

    ax_sig.scatter(buy.index, buy['Close'], marker='^', label='BUY')
    ax_sig.scatter(sell.index, sell['Close'], marker='v', label='SELL')

    ax_sig.legend()
    st.pyplot(fig_sig)

    # ================= TRADE HISTORY =================
    st.subheader("📄 Trade History")

    if not trades:
        st.write("No trades executed")
    else:
        # Header
        h1, h2 = st.columns([1, 2])
        h1.markdown("**Type**")
        h2.markdown("**Price**")

        # Rows
        for t, p in trades:
            c1, c2 = st.columns([1, 2])
            c1.write(t)
            c2.write(f"{p:.2f}")