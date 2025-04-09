import pandas as pd
from datetime import datetime
import requests

def get_binance_data(symbol='BTCEUR', interval='1h', limit=1000):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    
    response = requests.get(url, params=params)

    # Verifica se houve erro na resposta
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Erro ao acessar Binance API: {e}")
        return pd.DataFrame()

    data = response.json()

    # Verifica se a resposta parece válida
    if not isinstance(data, list):
        print("Resposta inesperada da API:", data)
        return pd.DataFrame()

    # Processa os dados
    processed = []
    for k in data:
        try:
            processed.append({
                'timestamp': datetime.utcfromtimestamp(k[0] / 1000),
                'open': float(k[1]),
                'high': float(k[2]),
                'low': float(k[3]),
                'close': float(k[4]),
                'volume': float(k[5])
            })
        except (IndexError, ValueError):
            print("Erro ao processar kline:", k)
            continue

    df = pd.DataFrame(processed)
    if df.empty:
        print("Nenhum dado válido foi processado.")
        return df

    df.set_index('timestamp', inplace=True)
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()

    return df.dropna()
