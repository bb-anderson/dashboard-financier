import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

st.title("📊 Dashboard Financier")

tickers_par_secteur = {
    "🖥️ Tech": ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "ORCL"],
    "🏦 Finance": ["JPM", "V", "MA", "BAC", "WFC", "GS", "MS", "BLK", "AXP"],
    "🏥 Sante": ["JNJ", "UNH", "ABBV", "MRK", "LLY", "PFE", "TMO", "ABT"],
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
        ticker2 = st.selectbox("Ticker a comparer", tickers_par_secteur[secteur2], key="t2")
    else:
        ticker2 = ""

periode = st.selectbox("Periode", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3, key="p1")

if ticker:
    data = yf.download(ticker, period=periode)
    data.columns = [col[0] for col in data.columns]
    data['MA50'] = data['Close'].rolling(window=50).mean()
    close = data['Close'].squeeze()
    rendements = close.pct_change().dropna()

    titre = f"{ticker} vs {ticker2}" if ticker2 else f"Cours de {ticker}"
    st.subheader(f"{titre} sur {periode}")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

    if ticker2:
        data2 = yf.download(ticker2, period=periode)
        data2.columns = [col[0] for col in data2.columns]
        close2 = data2['Close'].squeeze()
        data_norm = close / close.iloc[0] * 100
        data2_norm = close2 / close2.iloc[0] * 100
        ax1.plot(data_norm, label=ticker, color='blue')
        ax1.plot(data2_norm, label=ticker2, color='red')
        ax1.set_ylabel("Performance normalisee base 100")
    else:
        ax1.plot(close, label='Prix', color='blue')
        ax1.plot(data['MA50'], label='MA50', color='orange')
        ax1.set_ylabel("Prix USD")

    rolling_max = close.cummax()
    drawdown = (close - rolling_max) / rolling_max * 100
    ax2.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.4, label='Drawdown')
    ax2.set_ylabel("Drawdown %")
    ax2.grid(True)

    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig)

    rendement_total = ((close.iloc[-1] / close.iloc[0]) - 1) * 100
    volatilite = rendements.std() * np.sqrt(252) * 100
    taux_sans_risque = 0.05
    sharpe = (rendement_total/100 - taux_sans_risque) / (volatilite/100) if volatilite != 0 else 0
    rendements_negatifs = rendements[rendements < 0]
    sortino = (rendement_total/100 - taux_sans_risque) / (rendements_negatifs.std() * np.sqrt(252)) if len(rendements_negatifs) > 0 else 0
    mdd = drawdown.min()

    spy = yf.download("SPY", period=periode)
    spy.columns = [col[0] for col in spy.columns]
    spy_ret = spy['Close'].squeeze().pct_change().dropna()
    common = rendements.index.intersection(spy_ret.index)
    if len(common) > 10:
        cov = np.cov(rendements[common], spy_ret[common])[0][1]
        var_spy = np.var(spy_ret[common])
        beta = cov / var_spy if var_spy != 0 else 1
    else:
        beta = 1

    pires_jours = rendements.nsmallest(5) * 100
    pires_jours.index = pires_jours.index.strftime('%Y-%m-%d')

    if ticker2:
        perf_ticker2 = ((close2.iloc[-1] / close2.iloc[0]) - 1) * 100
        gagnant = ticker if rendement_total > perf_ticker2 else ticker2
        st.info(f"📊 Sur {periode}, {ticker} affiche +{rendement_total:.1f}% vs {ticker2} +{perf_ticker2:.1f}%. {gagnant} surperforme. Sharpe {ticker} : {sharpe:.2f}.")
    else:
        tendance = "au-dessus" if close.iloc[-1] > data['MA50'].squeeze().iloc[-1] else "en dessous"
        qualite = 'excellente' if sharpe > 2 else 'bonne' if sharpe > 1 else 'faible'
        st.info(f"📊 {ticker} affiche +{rendement_total:.1f}% sur {periode}, {tendance} de sa MA50. Sharpe {sharpe:.2f} — {qualite} performance ajustee du risque. Max Drawdown {mdd:.1f}%.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Prix actuel", f"{close.iloc[-1]:.2f}$")
    col2.metric("Rendement", f"{rendement_total:.2f}%")
    col3.metric("Volatilite ann.", f"{volatilite:.2f}%")
    col4.metric("Prix max", f"{close.max():.2f}$")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Sharpe", f"{sharpe:.2f}")
    col6.metric("Sortino", f"{sortino:.2f}")
    col7.metric("Max Drawdown", f"{mdd:.2f}%")
    col8.metric("Beta (vs SPY)", f"{beta:.2f}")

    st.subheader("🔴 5 pires journees")
    for date, val in pires_jours.items():
        st.write(f"{date} : {val:.2f}%")
