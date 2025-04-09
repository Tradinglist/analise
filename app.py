import streamlit as st
import requests
from binance_data import get_binance_data
from analyze_data import plot_chart
from model import train_model

# Página principal
st.set_page_config(page_title="Previsão de Criptomoedas", layout="wide")
st.title("📈 Previsão de Preço de Criptomoedas em EUR")

# Lista manual de pares que funcionam bem (evita erro 451)
available_pairs = ["BTCUSDT", "ETHEUR", "BNBEUR", "XRPEUR", "ADAEUR", "SOLEUR"]
symbol = st.selectbox("Escolha o par de criptomoeda:", available_pairs)
crypto_name = symbol.replace("EUR", "")

# Coletar dados da API
with st.spinner(f"🔄 Carregando dados para {symbol}..."):
    df = get_binance_data(symbol)

# Verificar se os dados são válidos
if df.empty or 'close' not in df.columns or 'open' not in df.columns:
    st.error(f"❌ Dados indisponíveis para o par {symbol}.")
else:
    # Plotar gráficos
    try:
        price_fig, macd_fig = plot_chart(df, crypto_name)
        st.plotly_chart(price_fig, use_container_width=True)
        st.plotly_chart(macd_fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráficos: {e}")

    # Previsão com ML
    st.subheader(f"📊 Previsão para a próxima hora ({symbol})")
    try:
        prediction, report = train_model(df)
        if prediction == 1:
            st.markdown(f"### 🟢 O modelo prevê que o preço do **{crypto_name}** vai **subir**.")
        else:
            st.markdown(f"### 🔴 O modelo prevê que o preço do **{crypto_name}** vai **cair**.")

        # Exibir métricas do modelo
        st.subheader("📋 Desempenho do Modelo")
        st.json(report)
    except Exception as e:
        st.error(f"Erro ao treinar modelo ou prever: {e}")
