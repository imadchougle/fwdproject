from utils import *
import json
from utils import *
from fyers_apiv3 import fyersModel


def get_latest_ltp():
    apicredfile = open('UserCred.json')
    UserCred = json.load(apicredfile)

    with open('Tokens/access_token.txt', 'r') as file:
        token = file.read().strip()

    client_id = UserCred["client_id"]

    fyers = fyersModel.FyersModel(client_id=client_id,
                                  is_async=False,
                                  token=token
                                  )
    stock_ltp = []

    for i in range(len(scripts)):
        data = {
                "symbols": "NSE:" + scripts[i] + "-EQ"
            }
        response = fyers.quotes(data=data)
        ltp = response.get("d", [])[0].get("v", {}).get("lp")

        stock_ltp.append(ltp)

    return stock_ltp