from binance.client import Client
from datetime import datetime
import pandas as pd

def get_binance_data(symbol='BTCEUR', interval='1h', lookback='365 days ago UTC'):
    client = Client()
    klines = client.get_historical_klines(symbol, interval, lookback)

    data = []
    for k in klines:
        data.append({
            'timestamp': datetime.utcfromtimestamp(k[0] / 1000),
            'open': float(k[1]),
            'high': float(k[2]),
            'low': float(k[3]),
            'close': float(k[4]),
            'volume': float(k[5])
        })

    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()
    return df.dropna()