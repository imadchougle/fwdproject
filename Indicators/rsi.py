import pandas as pd
from fyers_apiv3 import fyersModel
import json
import pandas_ta as ta
from utils import scripts

apicredfile = open('C:\\Users\\imadc\\PycharmProjects\\fwdproject\\UserCred.json')
UserCred = json.load(apicredfile)

FROM_DATE = '2023-08-08'
TO_DATE = '2024-01-17'  # current date

with open('C:\\Users\\imadc\\PycharmProjects\\fwdproject\\Tokens\\access_token.txt', 'r') as file:
    token = file.read().strip()

client_id = UserCred["client_id"]
secret_key = UserCred["secret_id"]
redirect_uri = UserCred["redirect_uri"]
response_type = UserCred["response_type"]
state = UserCred["state"]
grant_type = UserCred["grant_type"]

fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=token)

result_data = []

for stocks in range(len(scripts)):
    data = {
        "symbol": "NSE:" + scripts[stocks] + "-EQ",
        "resolution": "D",
        "date_format": "1",
        "range_from": FROM_DATE,
        "range_to": TO_DATE,
        "cont_flag": "1"
    }

    close_value = []
    high_value = []
    low_value = []

    response = fyers.history(data=data)

    candles = response['candles']

    for candle in candles:
        close_value.append(candle[4])
        high_value.append(candle[2])
        low_value.append(candle[3])

    df = pd.DataFrame({'High': high_value,  'Low': low_value, 'Close': close_value})
    df['ADX'] = ta.adx(high=df['High'], low=df['Low'], close=df['Close'], length=14, detailed=False)['ADX_14']
    df['Awesome_Oscillator'] = ta.ao(df['High'], df['Low'])
    df['CCI'] = ta.cci(high=df['High'], low=df['Low'], close=df['Close'], length=14)

    macd_values = ta.macd(df['Close'], fast=12, slow=26, signal=9)
    macd_values.columns = ['MACD_Line', 'MACD_Histogram', 'MACD_Signal_Line']

    bollinger_bands = ta.bbands(df['Close'], length=20)
    bollinger_bands = bollinger_bands[['BBU_20_2.0', 'BBL_20_2.0', 'BBM_20_2.0']]
    bollinger_bands.columns = ['Upper_Band', 'Lower_Band', 'Basis']


    latest_rsi = df.ta.rsi(length=14).iloc[-1] # RSI

    latest_adx = df.iloc[-1]['ADX'] # ADX

    latest_awesome_oscillator = df.iloc[-1]['Awesome_Oscillator'] # AO

    latest_cci = df.iloc[-1]['CCI'] # CCI

    latest_macd_line = macd_values['MACD_Line'].iloc[-1]    # MACD
    latest_histo_line = macd_values['MACD_Histogram'].iloc[-1]
    latest_signal_line = macd_values['MACD_Signal_Line'].iloc[-1]

    latest_upper_bb = bollinger_bands['Upper_Band'].iloc[-1]
    latest_lower_bb = bollinger_bands['Lower_Band'].iloc[-1]
    latest_basis_bb = bollinger_bands['Basis'].iloc[-1]

    result_data.append({'Stocks': scripts[stocks],
                        'RSI': latest_rsi,
                        'ADX': latest_adx,
                        'Awesome_Oscillator': latest_awesome_oscillator,
                        'Commodity Channel Index': latest_cci,
                        'MACD_Line': latest_macd_line,
                        'MACD_Signal_Line': latest_signal_line,
                        'MACD_Histogram': latest_histo_line,
                        'BB_Upper' : latest_upper_bb,
                        'BB_Lower' : latest_lower_bb,
                        'BB_Basis' : latest_basis_bb
                        })

result_df = pd.DataFrame(result_data)
print(result_df)
result_df.to_csv('indicators.csv', index=False)
