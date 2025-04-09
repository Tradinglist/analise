import pandas as pd
from datetime import datetime
import requests

# Função para coletar dados históricos sem autenticação
def get_binance_data(symbol='BTCEUR', interval='1h', limit=1000):
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    data = response.json()

    processed = []
    for k in data:
        processed.append({
            'timestamp': datetime.utcfromtimestamp(k[0] / 1000),
            'open': float(k[1]),
            'high': float(k[2]),
            'low': float(k[3]),
            'close': float(k[4]),
            'volume': float(k[5]),
        })

    df = pd.DataFrame(processed)
    df.set_index('timestamp', inplace=True)

    # Cálculo de médias móveis
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()

    return df.dropna()
