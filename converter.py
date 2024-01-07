import xlwings as xw
import pandas as pd

csv_file_path = 'csv_files/Combined_with_LTP.csv'
excel_file_path = 'converted_data.xlsx'

df = pd.read_csv(csv_file_path)

wb = xw.Book()

wb.sheets[0].range('A1').options(index=False).value = df

wb.save(excel_file_path)

wb.close()

print(f'Converted CSV to Excel. Excel file saved at: {excel_file_path}')
