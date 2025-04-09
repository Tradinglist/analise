# Previsão de Preço de Criptomoedas (BTC, SOL, ADA em EUR)

Este projeto utiliza dados públicos da Binance e um modelo de regressão logística para prever se o preço das criptos BTC, SOL e ADA vai subir ou cair na próxima hora.

## Funcionalidades

- Coleta automática dos dados da Binance (1h de intervalo)
- Análise técnica com médias móveis (SMA, EMA) e MACD
- Treinamento de modelo de machine learning (Logistic Regression)
- Interface com Streamlit para visualização interativa

## Requisitos

Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como rodar

```bash
streamlit run app.py
```

## Estrutura do Projeto

```
crypto_predictor/
├── app.py             # Interface principal com Streamlit
├── binance_data.py    # Coleta de dados da Binance
├── analyze_data.py    # Gráficos interativos
├── model.py           # Machine Learning
├── requirements.txt   # Pacotes necessários
└── README.md          # Documentação
```