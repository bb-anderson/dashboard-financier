import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("Dashboard Financier")

ticker = st.text_input("Entrez un ticker", value="AAPL")

if ticker:
    data = yf.download(ticker, period="1y")
    data.columns = [col[0] for col in data.columns]
    data['MA50'] = data['Close'].rolling(window=50).mean()
    
    st.subheader(f"Cours de {ticker} sur 1 an")
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(data['Close'], label='Prix', color='blue')
    ax.plot(data['MA50'], label='MA50', color='orange')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)    
    col1, col2, col3, col4 = st.columns(4)

rendement = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
volatilite = data['Close'].pct_change().std() * 100

col1.metric("Prix actuel", f"{data['Close'].iloc[-1]:.2f}$")
col2.metric("Rendement 1 an", f"{rendement:.2f}%")
col3.metric("Volatilité", f"{volatilite:.2f}%")
col4.metric("Prix max", f"{data['Close'].max():.2f}$")

