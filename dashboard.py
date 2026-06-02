import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("📊 Dashboard Financier")

tickers_par_secteur = {
    "🖥️ Tech": ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "ORCL"],
    "🏦 Finance": ["JPM", "V", "MA", "BAC", "WFC", "GS", "MS", "BLK", "AXP"],
    "🏥 Santé": ["JNJ", "UNH", "ABBV", "MRK", "LLY", "PFE", "TMO", "ABT"],
    "🛒 Conso": ["WMT", "PG", "KO", "PEP", "COST", "MCD", "NKE", "SBUX"],
    "⚡ Energie": ["XOM", "CVX", "COP", "SLB", "EOG", "OXY"],
    "🏗️ Industrie": ["CAT", "HON", "UPS", "BA", "RTX", "GE", "MMM", "DE"],
    "🇪🇺 Europe": ["ASML", "TTE.PA", "MC.PA", "BNP.PA", "AIR.PA", "OR.PA"],
    "🌏 Asie": ["TSM", "BABA", "SONY", "TM", "005930.KS"],
    "📊 ETF/Indices": ["SPY", "QQQ", "DIA", "GLD", "TLT"]
}

col_input1, col_input2 = st.columns(2)

with col_input1:
    secteur1 = st.selectbox("Secteur", list(tickers_par_secteur.keys()), key="s1")
    ticker = st.selectbox("Ticker principal", tickers_par_secteur[secteur1], key="t1")

with col_input2:
    comparer = st.checkbox("Comparer avec une autre action")
    if comparer:
        secteur2 = st.selectbox("Secteur", list(tickers_par_secteur.keys()), key="s2")
        ticker2 = st.selectbox("Ticker à comparer", tickers_par_secteur[secteur2], key="t2")
    else:
        ticker2 = ""

periode = st.selectbox("Période d'analyse", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3, key="p1")

if ticker:
    data = yf.download(ticker, period=periode)
    data.columns = [col[0] for col in data.columns]
    data['MA50'] = data['Close'].rolling(window=50).mean()

    st.subheader(f"Cours de {ticker} sur {periode}")
    fig, ax = plt.subplots(figsize=(12, 5))

    if ticker2:
        data2 = yf.download(ticker2, period=periode)
        data2.columns = [col[0] for col in data2.columns]
        data_norm = data['Close'] / data['Close'].iloc[0] * 100
        data2_norm = data2['Close'] / data2['Close'].iloc[0] * 100
        ax.plot(data_norm, label=ticker, color='blue')
        ax.plot(data2_norm, label=ticker2, color='red')
        ax.set_ylabel("Performance normalisée (base 100)")
    else:
        ax.plot(data['Close'], label='Prix', color='blue')
        ax.plot(data['MA50'], label='MA50', color='orange')
        ax.set_ylabel("Prix (USD)")

    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    col1, col2, col3, col4 = st.columns(4)
    close_prices = data['Close'].squeeze()
    rendement = ((close_prices.iloc[-1] / close_prices.iloc[0]) - 1) * 100
    volatilite = close_prices.pct_change().std() * 100

    col1.metric("Prix actuel", f"{close_prices.iloc[-1]:.2f}$")
    col2.metric("Rendement", f"{rendement:.2f}%")
    col3.metric("Volatilite", f"{volatilite:.2f}%")
    col4.metric("Prix max", f"{close_prices.max():.2f}$")
