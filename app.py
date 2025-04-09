import streamlit as st
from binance_data import get_binance_data
from analyze_data import plot_chart
from model import train_model

# ✅ Parâmetros fixos (sem chamadas bloqueadas à API externa)
available_pairs = ["BTCEUR", "ETHEUR", "BNBEUR", "XRPEUR", "ADAEUR", "SOLEUR"]

# Configuração da interface
st.set_page_config(page_title="Previsão de Criptomoedas", layout="wide")
st.title("📈 Previsão de Preço de Criptomoedas em EUR")

# Seleção da criptomoeda
symbol = st.selectbox("Escolha o par de criptomoeda:", available_pairs)
crypto_name = symbol.replace("EUR", "")

# Obtenção dos dados históricos da Binance
with st.spinner(f"🔄 Carregando dados para {symbol}..."):
    df = get_binance_data(symbol)

# Verifica se os dados são válidos
if df.empty or 'close' not in df.columns or 'open' not in df.columns:
    st.error(f"❌ Dados indisponíveis para o par {symbol}.")
else:
    # Geração dos gráficos interativos
    try:
        price_fig, macd_fig = plot_chart(df, crypto_name)
        st.plotly_chart(price_fig, use_container_width=True)
        st.plotly_chart(macd_fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráficos: {e}")

    # Previsão com modelo de machine learning
    st.subheader(f"📊 Previsão para a próxima hora ({symbol})")
    try:
        prediction, report = train_model(df)

        if prediction == 1:
            st.markdown(f"### 🟢 O modelo prevê que o preço do **{crypto_name}** vai **subir**.")
        else:
            st.markdown(f"### 🔴 O modelo prevê que o preço do **{crypto_name}** vai **cair**.")

        # Exibição do desempenho do modelo
        st.subheader("📋 Desempenho do Modelo")
        st.json(report)
    except Exception as e:
        st.error(f"Erro ao treinar modelo ou prever: {e}")
