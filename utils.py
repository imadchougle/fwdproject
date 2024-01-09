import pandas as pd

scripts = ['AARTIIND', 'ABB', 'ABBOTINDIA', 'ABCAPITAL', 'ABFRL']


def fib(high, low):
    diff = high - low
    return [
        high,
        round(low + (diff * 0), 2),
        round(low + (diff * 0.236), 2),
        round(low + (diff * 0.382), 2),
        round(low + (diff * 0.50), 2),
        round(low + (diff * 0.618), 2),
        round(low + (diff * 0.786), 2),
        round(low + (diff * 1), 2),
        round(low + (diff * 1.236), 2),
        round(low + (diff * 1.618), 2),
        low
    ]


def getMaxHigh(data):
    return data['High'].max()


def getMinLow(data):
    return data['Low'].min()


def processData(data):
    return pd.DataFrame(data, columns =['epoch_time', 'Open', 'High', 'Low', 'Close', 'volume'])