import pandas as pd
from fyers_apiv3 import fyersModel
import json
import pandas_ta as ta
from utils import scripts

apicredfile = open('C:\\Users\\imadc\\PycharmProjects\\fwdproject\\UserCred.json')
UserCred = json.load(apicredfile)

FROM_DATE = '2023-08-10'  #last 110 candles date
TO_DATE = '2024-01-19'  # current date

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
    volume_value = []

    response = fyers.history(data=data)

    candles = response['candles']

    for candle in candles:
        close_value.append(candle[4])
        high_value.append(candle[2])
        low_value.append(candle[3])
        volume_value.append(candle[5])

    df = pd.DataFrame({'High': high_value,  'Low': low_value, 'Close': close_value, 'Volume': volume_value})

# -------------------------------------------------------------------------------------------------------------
    df['RSI'] = ta.rsi(close=df['Close'], length=14)
    df['ADX'] = ta.adx(high=df['High'], low=df['Low'], close=df['Close'], length=14, detailed=False)['ADX_14']
    df['Awesome_Oscillator'] = ta.ao(df['High'], df['Low'])
    df['CCI'] = ta.cci(high=df['High'], low=df['Low'], close=df['Close'], length=14)

    macd_values = ta.macd(df['Close'], fast=12, slow=26, signal=9)
    macd_values.columns = ['MACD_Line', 'MACD_Histogram', 'MACD_Signal_Line']

    bollinger_bands = ta.bbands(df['Close'], length=20)
    bollinger_bands = bollinger_bands[['BBU_20_2.0', 'BBL_20_2.0', 'BBM_20_2.0']]
    bollinger_bands.columns = ['Upper_Band', 'Lower_Band', 'Basis']

    money_flow_index = ta.mfi(df['High'], df['Low'], df['Close'], df['Volume'], length=14)

    df['SMA20'] = ta.sma(df['Close'], length=20)
    df['SMA50'] = ta.sma(df['Close'], length=50)
    df['SMA100'] = ta.sma(df['Close'], length=100)
    df['SMA200'] = ta.sma(df['Close'], length=200)

    stochrsi_values = ta.stochrsi(close=df['Close'], length=14, k=3, d=3)
    df['StochRSI_K'] = stochrsi_values.iloc[:, 0]
    df['StochRSI_D'] = stochrsi_values.iloc[:, 1]

    # Stochastic Oscillator (stoch)
    stoch_values = ta.stoch(df['High'], df['Low'], df['Close'], k=14, d=3, smooth_k=3)
    df['Stoch_K'] = stoch_values.iloc[:, 0]

# ---------------------------------------------------------------------------------
    latest_rsi = round(df.iloc[-1]['RSI'], 2) # RSI

    latest_adx = round(df.iloc[-1]['ADX'], 2) # ADX

    latest_awesome_oscillator = round(df.iloc[-1]['Awesome_Oscillator'], 2) # AO

    latest_cci = round(df.iloc[-1]['CCI'], 2) # CCI

    latest_macd_line = round(macd_values['MACD_Line'].iloc[-1], 2)  # MACD
    latest_histo_line = round(macd_values['MACD_Histogram'].iloc[-1], 2)
    latest_signal_line = round(macd_values['MACD_Signal_Line'].iloc[-1], 2)

    latest_upper_bb = round(bollinger_bands['Upper_Band'].iloc[-1], 2) # Bollinger Bands
    latest_lower_bb = round(bollinger_bands['Lower_Band'].iloc[-1], 2)
    latest_basis_bb = round(bollinger_bands['Basis'].iloc[-1], 2)

    latest_mfi = round(money_flow_index.iloc[-1], 2)

    latest_sma20 = round(df.iloc[-1]['SMA20'], 2)
    latest_sma50 = round(df.iloc[-1]['SMA50'], 2)
    latest_sma100 = round(df.iloc[-1]['SMA100'], 2)
    latest_sma200 = df.iloc[-1]['SMA200']

    latest_stochrsi_k = round(df.iloc[-1]['StochRSI_K'], 2)  # StochRSI K
    latest_stochrsi_d = round(df.iloc[-1]['StochRSI_D'], 2)  # StochRSI D

    latest_stoch_k = round(df.iloc[-1]['Stoch_K'], 2)

# ------------------------------------------------------------------------------------------------------------

    result_data.append({'Stocks': scripts[stocks],
                        'RSI': latest_rsi,
                        'ADX': latest_adx,
                        'Awesome_Oscillator': latest_awesome_oscillator,
                        'Commodity Channel Index': latest_cci,
                        'MACD_Line': latest_macd_line,
                        'MACD_Signal_Line': latest_signal_line,
                        'MACD_Histogram': latest_histo_line,
                        'BB_Upper': latest_upper_bb,
                        'BB_Lower': latest_lower_bb,
                        'BB_Basis': latest_basis_bb,
                        'MFI': latest_mfi,
                        'SMA20': latest_sma20,
                        'SMA50': latest_sma50,
                        'SMA100': latest_sma100,
                        'SMA200': latest_sma200,
                        'StochRSI_K': latest_stochrsi_k,
                        'StochRSI_D': latest_stochrsi_d,
                        'Stochastic Oscillator': latest_stoch_k
                        })

result_df = pd.DataFrame(result_data)
print(result_df)
result_df.to_csv('indicators.csv', index=False)