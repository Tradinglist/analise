import streamlit as st
import requests
from binance_data import get_binance_data
from analyze_data import plot_chart
from model import train_model

# Busca pares EUR disponíveis na Binance (BTC, ETH, ADA, etc.)
@st.cache_data(ttl=3600)
def get_available_eur_pairs(allowed_bases=['BTC', 'ETH', 'ADA', 'SOL', 'BNB', 'XRP']):
    url = "https://api.binance.com/api/v3/exchangeInfo"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pairs = [s['symbol'] for s in data['symbols']]
        eur_pairs = [p for p in pairs if p.endswith('EUR')]
        valid_pairs = [p for p in eur_pairs if p.replace('EUR', '') in allowed_bases]
        return sorted(valid_pairs)
    except Exception as e:
        st.error(f"Erro ao buscar pares EUR da Binance: {e}")
        return []

# Página principal
st.set_page_config(page_title="Previsão de Criptomoedas", layout="wide")
st.title("📈 Previsão de Preço de Criptomoedas em EUR")

# Carregar pares EUR disponíveis
available_pairs = get_available_eur_pairs()
if not available_pairs:
    st.error("❌ Nenhum par EUR disponível encontrado na Binance no momento.")
    st.stop()

# Seleção do par válido
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
