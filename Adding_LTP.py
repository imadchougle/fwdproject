import xlwings as xw
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


latest_ltp = get_latest_ltp()


def adding_ltp_column():
    file_path = 'csv_files/merged_data_without_LTP.xlsx'
    wb = xw.Book(file_path)
    sheet = wb.sheets[0]

    sheet.range('B:B').api.Insert(Shift=-4161)  # -4161 corresponds to shifting to the right
    sheet.range('B1').value = 'ltp'

    data_list = latest_ltp

    cell_to_add = 'B2'
    sheet.range(cell_to_add).options(transpose=True).value = data_list

    wb.save('csv_files/merged_data_with_ltp.xlsx')
    wb.close()


adding_ltp_column()