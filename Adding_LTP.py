import xlwings as xw
import json
from utils import *
from fyers_apiv3 import fyersModel
from get_LTP_from_here import *


latest_ltp = get_latest_ltp()


def adding_ltp_column():
    file_path = 'csv_files/merged_data_without_LTP.xlsx'
    wb = xw.Book(file_path)
    sheet = wb.sheets[0]

    sheet.range('B:B').api.Insert(Shift=-4161)  # -4161 corresponds to shifting to the right
    sheet.range('B2').value = 'ltp'

    data_list = latest_ltp

    cell_to_add = 'B3'
    sheet.range(cell_to_add).options(transpose=True).value = data_list

    wb.save('csv_files/merged_data_with_ltp.xlsx')
    wb.close()


adding_ltp_column()