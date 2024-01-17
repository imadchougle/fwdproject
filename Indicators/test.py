import pandas as pd
from fyers_apiv3 import fyersModel
import json
import pandas_ta as ta
from utils import scripts

apicredfile = open('C:\\Users\\imadc\\PycharmProjects\\fwdproject\\UserCred.json')
UserCred = json.load(apicredfile)

FROM_DATE = '2023-08-07'
TO_DATE = '2024-01-16'  # current date

with open('C:\\Users\\imadc\\PycharmProjects\\fwdproject\\Tokens\\access_token.txt', 'r') as file:
    token = file.read().strip()

client_id = UserCred["client_id"]
secret_key = UserCred["secret_id"]
redirect_uri = UserCred["redirect_uri"]
response_type = UserCred["response_type"]
state = UserCred["state"]
grant_type = UserCred["grant_type"]

fyers = fyersModel.FyersModel(client_id=client_id,
                              is_async=False,
                              token=token)

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

    last_adx = df.iloc[-1]
    print(scripts[stocks], last_adx['ADX'])
