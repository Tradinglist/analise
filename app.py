import streamlit as st
from binance_data import get_binance_data
from analyze_data import plot_chart
from model import train_model

# Configuração da interface
st.set_page_config(page_title="Previsão de Criptomoedas", layout="wide")
st.title("📈 Previsão de Preço de Criptomoedas em EUR")

# Escolha da criptomoeda
crypto_option = st.selectbox("Escolha a criptomoeda:", ["BTC", "SOL", "ADA"])
symbol = f"{crypto_option}EUR"

# Coleta dos dados
with st.spinner(f"🔄 Carregando dados para {symbol}..."):
    df = get_binance_data(symbol)

# Verifica se os dados foram carregados corretamente
if df.empty or 'close' not in df.columns or 'open' not in df.columns:
    st.error("❌ Não foi possível carregar os dados da Binance ou o par escolhido não está disponível.")
else:
    # Gráficos interativos
    try:
        price_fig, macd_fig = plot_chart(df, crypto_option)
        st.plotly_chart(price_fig, use_container_width=True)
        st.plotly_chart(macd_fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráficos: {e}")
    
    # Previsão
    st.subheader(f"📊 Previsão para a próxima hora ({crypto_option}/EUR)")
    try:
        prediction, report = train_model(df)
        if prediction == 1:
            st.markdown(f"### 🟢 O modelo prevê que o preço do **{crypto_option}** vai **subir**.")
        else:
            st.markdown(f"### 🔴 O modelo prevê que o preço do **{crypto_option}** vai **cair**.")

        # Métricas do modelo
        st.subheader("📋 Desempenho do Modelo")
        st.json(report)
    except Exception as e:
        st.error(f"Erro ao treinar modelo ou prever: {e}")
