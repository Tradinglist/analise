import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

def train_model(df):
    df['EMA_100'] = df['close'].ewm(span=100, adjust=False).mean()
    df['EMA_100_diff'] = df['EMA_100'].diff()
    df['MACD'] = df['close'].ewm(span=12, adjust=False).mean() - df['close'].ewm(span=26, adjust=False).mean()
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['price_change'] = df['close'].pct_change()
    df['price_diff'] = df['close'].diff()
    df['SMA_50_diff'] = df['SMA_50'].diff()
    df.dropna(inplace=True)
    df['target'] = (df['price_change'].shift(-1) > 0).astype(int)

    X = df[['price_change', 'price_diff', 'SMA_50_diff', 'EMA_100_diff', 'MACD', 'MACD_Signal', 'open']]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    report = classification_report(y_test, y_pred, output_dict=True)

    latest = scaler.transform([X.iloc[-1]])
    prediction = model.predict(latest)[0]

    return prediction, report