import xlwings as xw


def extract_45_days_fib_values(file_path, start_cell):

    wb = xw.Book(file_path)
    sheet = wb.sheets[0]
    values = sheet.range(start_cell).expand('down').value
    wb.close()

    return values

file_path = 'csv_files/merged_data_with_ltp.xlsx'
start_cell_to_extract_45_days = 'C3 :  K3'

d45_fib_prices = extract_45_days_fib_values(file_path, start_cell_to_extract_45_days)