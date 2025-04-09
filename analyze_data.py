import plotly.graph_objects as go

def add_technical_indicators(df):
    df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['EMA_100'] = df['close'].ewm(span=100, adjust=False).mean()
    return df

def plot_chart(df, symbol='BTC'):
    df = add_technical_indicators(df)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['close'], mode='lines', name='Fechamento', line=dict(color='cyan')))
    fig.add_trace(go.Scatter(x=df.index, y=df['open'], mode='lines', name='Abertura', line=dict(color='orange', dash='dot')))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], mode='lines', name='SMA 50', line=dict(dash='dot')))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], mode='lines', name='SMA 200', line=dict(dash='dot')))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_100'], mode='lines', name='EMA 100', line=dict(dash='dash')))

    fig.update_layout(title=f'Análise Técnica do {symbol}/EUR', xaxis_title='Data', yaxis_title='Preço (€)', template='plotly_dark', height=600)

    macd_fig = go.Figure()
    macd_fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='lightgreen')))
    macd_fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name='Sinal', line=dict(color='red')))
    macd_fig.update_layout(title='MACD (Indicador de Momento)', xaxis_title='Data', yaxis_title='Valor', template='plotly_dark', height=300)

    return fig, macd_fig