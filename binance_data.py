import pandas as pd
from datetime import datetime
import requests

def get_binance_data(symbol='BTCEUR', interval='1h', limit=1000):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Verificação extra
        if not isinstance(data, list) or len(data) == 0:
            print(f"⚠️ Resposta inesperada da API para {symbol}: {data}")
            return pd.DataFrame()

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
            except (IndexError, ValueError) as e:
                print(f"Erro ao processar linha: {k} -> {e}")
                continue

        df = pd.DataFrame(processed)

        if df.empty:
            print(f"❌ Nenhum dado processado para {symbol}")
            return df

        df.set_index('timestamp', inplace=True)
        df['SMA_50'] = df['close'].rolling(window=50).mean()
        df['SMA_200'] = df['close'].rolling(window=200).mean()

        return df.dropna()

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição à Binance: {e}")
        return pd.DataFrame()
