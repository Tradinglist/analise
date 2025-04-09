import streamlit as st
from binance_data import get_binance_data
from analyze_data import plot_chart
from model import train_model

st.set_page_config(page_title="Previsão de Criptomoedas", layout="wide")
st.title("📈 Previsão de Preço de Criptomoedas em EUR")

crypto_option = st.selectbox("Escolha a criptomoeda:", ["BTC", "SOL", "ADA"])
symbol = f"{crypto_option}EUR"

with st.spinner(f"🔄 Carregando dados para {symbol}..."):
    df = get_binance_data(symbol)

st.success("✅ Dados carregados!")
price_fig, macd_fig = plot_chart(df, crypto_option)
st.plotly_chart(price_fig, use_container_width=True)
st.plotly_chart(macd_fig, use_container_width=True)

st.subheader(f"📊 Previsão para a próxima hora ({crypto_option}/EUR)")
prediction, report = train_model(df)

if prediction == 1:
    st.markdown(f"### 🟢 O modelo prevê que o preço do **{crypto_option}** vai **subir**.")
else:
    st.markdown(f"### 🔴 O modelo prevê que o preço do **{crypto_option}** vai **cair**.")

st.subheader("📋 Desempenho do Modelo")
st.json(report)