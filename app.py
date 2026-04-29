import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from data_loader import load_data
from features import create_features
from ai_model import train_model, generate_signals
from strategy import apply_strategy
from backtester import run_backtest
from metrics import calculate_metrics

# Page config (MUST be first Streamlit command)
st.set_page_config(page_title="Trading AI Platform", layout="wide")

# Sidebar
st.sidebar.header("⚙️ Configuration")

symbol = st.sidebar.text_input("Symbol", "AAPL")
strategy_type = st.sidebar.selectbox("Strategy", ["Rule-Based", "AI-Based"])
initial_balance = st.sidebar.number_input("Initial Balance", value=10000)
auto_mode = st.sidebar.checkbox("Enable Auto Trading (Paper)")

run = st.sidebar.button("Run Backtest")

# Dark theme
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
[data-testid="stSidebar"] { background-color: #111827; }
.stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 AI Trading Backtesting Dashboard")

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

    # 🔥 IMPORTANT (you missed this)
    final_value, trades, df = run_backtest(df, initial_balance)

    # Metrics
    results = calculate_metrics(initial_balance, final_value, df, trades)

    # ================= BASIC METRICS =================
    st.subheader("📊 Performance")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Initial", f"${results['Initial Balance']:.2f}")
    col2.metric("Final", f"${results['Final Balance']:.2f}")
    col3.metric("Return %", f"{results['Return %']:.2f}%")
    col4.metric("Drawdown", f"{results['Max Drawdown %']:.2f}%")

    # ================= ADVANCED METRICS =================
    st.subheader("📊 Advanced Metrics")
    c1, c2, c3 = st.columns(3)

    c1.metric("Sharpe Ratio", f"{results['Sharpe Ratio']:.2f}")
    c2.metric("Win Rate", f"{results['Win Rate %']:.2f}%")
    c3.metric("Profit Factor", f"{results['Profit Factor']:.2f}")

    # ================= CANDLESTICK =================
    st.subheader("🕯️ Candlestick Chart")

    fig_candle = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])

    # BUY markers
    buy_points = df[df['buy_signal']]
    fig_candle.add_trace(go.Scatter(
        x=buy_points.index,
        y=buy_points['Close'],
        mode='markers',
        name='BUY',
        marker=dict(symbol='triangle-up', size=10)
    ))

    # SELL markers
    sell_points = df[df['sell_signal']]
    fig_candle.add_trace(go.Scatter(
        x=sell_points.index,
        y=sell_points['Close'],
        mode='markers',
        name='SELL',
        marker=dict(symbol='triangle-down', size=10)
    ))

    fig_candle.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig_candle, width='stretch')

    # ================= EQUITY =================
    st.subheader("📈 Equity Curve")

    fig_equity = go.Figure()
    fig_equity.add_trace(go.Scatter(
        x=df.index,
        y=df['equity'],
        mode='lines',
        name='Equity'
    ))

    fig_equity.update_layout(template="plotly_dark", height=400)
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

    fig_dd.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig_dd, width='stretch')

    # ================= AUTO TRADING =================
    if auto_mode:
        st.subheader("🤖 Auto Trading Simulation")

        if df['buy_signal'].iloc[-1]:
            st.success("Bot would BUY now")
        elif df['sell_signal'].iloc[-1]:
            st.error("Bot would SELL now")
        else:
            st.info("No action")

    # ================= TRADE HISTORY =================
    st.subheader("📄 Trade History")

    if not trades:
        st.write("No trades executed")
    else:
        h1, h2 = st.columns([1, 2])
        h1.markdown("**Type**")
        h2.markdown("**Price**")

        for t, p in trades:
            c1, c2 = st.columns([1, 2])
            c1.write(t)
            c2.write(f"{p:.2f}")