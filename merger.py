import pandas as pd
import xlwings as xw


def merger():
    df_45_days = pd.read_csv('csv_files/D45_cycle.csv', index_col='stock')
    df_15_days = pd.read_csv('csv_files/D15_cycle.csv', index_col='stock')

    merged_df = pd.concat([df_45_days, df_15_days],
                          axis=1)

    wb = xw.Book()

    sheet = wb.sheets['Sheet1']
    sheet.range('A1').value = merged_df

    wb.save('csv_files/merged_data_without_LTP.xlsx')

    wb.close()
    print("Done Merging it")
