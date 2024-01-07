from fyers_apiv3 import fyersModel
import json
from utils import *
import xlwings as xw


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


result = get_latest_ltp()


def add_ltp_from_here():
    data_list = result
    wb = xw.Book('Combined_with_LTP.xlsx')
    sheet = xw.sheets[0]
    cell_to_add = 'B3'
    sheet.range(cell_to_add).options(transpose=True).value = data_list

    wb.save()
    wb.close()


add_ltp_from_here()