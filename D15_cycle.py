from fyers_apiv3 import fyersModel
import json
from utils import *
import pandas as pd
import time


apicredfile = open('UserCred.json')
UserCred = json.load(apicredfile)

FROM_DATE = '2023-12-15'
TO_DATE = '2023-12-29'


def get_access_token():
    try:
        with open('Tokens/access_token.txt', 'r') as file:
            access_token = file.read().strip()
        return access_token
    except FileNotFoundError:
        print("Error: access_token.txt not found.")
        return None


token = get_access_token()


client_id = UserCred["client_id"]
secret_key = UserCred["secret_id"]
redirect_uri = UserCred["redirect_uri"]
response_type = UserCred["response_type"]
state = UserCred["state"]
grant_type = UserCred["grant_type"]

fyers = fyersModel.FyersModel(client_id=client_id,
                              is_async=False,
                              token=token)

stock_data = []

for i in range(len(scripts)):
    data = {
        "symbol": "NSE:" + scripts[i] + "-EQ",
        "resolution": "D",
        "date_format": "1",
        "range_from": FROM_DATE,
        "range_to": TO_DATE,
        "cont_flag": "1"
    }

    response = fyers.history(data=data)

    process_data = processData(response['candles'])
    fib_values = fib(getMaxHigh(process_data), getMinLow(process_data))

    high_value = fib_values[0]
    fib_0 = fib_values[1]
    fib_236 = fib_values[2]
    fib_382 = fib_values[3]
    fib_50 = fib_values[4]
    fib_618 = fib_values[5]
    fib_786 = fib_values[6]
    fib_1 = fib_values[7]
    fib_1236 = fib_values[8]
    fib_1618 = fib_values[9]
    low_value = fib_values[10]

    stock_data.append([scripts[i], fib_0,fib_236, fib_382, fib_50, fib_618, fib_786, fib_1, fib_1236,fib_1618])

    if (i % 20 == 0):
        print("#", end='')

    time.sleep(0.1)

dataframe = pd.DataFrame(stock_data, columns=['stock', '0', '0.236', '0.382', '0.5', '0.618', '0.786', '1', '1.236','1.618'])

dataframe.to_csv(r"csv_files/D15_cycle.csv", index=False)

print()
print('Processing Done')