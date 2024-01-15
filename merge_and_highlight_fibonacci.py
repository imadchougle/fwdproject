import xlwings as xw
from utils import *
from get_LTP_from_here import *
import pandas as pd


def merge_and_add_ltp():
    df_45_days = pd.read_csv('csv_files/D45_cycle.csv', index_col='stock')
    df_15_days = pd.read_csv('csv_files/D15_cycle.csv', index_col='stock')

    merged_df = pd.concat([df_45_days, df_15_days],
                          axis=1,
                          keys=['45 days', '15 days'])

    wb = xw.Book()
    sheet = wb.sheets[0]

    sheet.range('A1').value = merged_df

    sheet.range('B:B').api.Insert(Shift=-4161)  # -4161 corresponds to shifting to the right
    sheet.range('B2').value = 'ltp'

    sheet.range('B3').options(transpose=True).value = latest_ltp

    wb.save('csv_files/merged_data_with_ltp.xlsx')
    wb.close()
    print("Done Merging and Adding 'ltp' Column.")


def new_highlight_matching_fib_levels():
    file_path = 'csv_files/merged_data_with_ltp.xlsx'
    column_mapping = {'C': 'L',
                      'D': 'M',
                      'E': 'N',
                      'F': 'O',
                      'G': 'P',
                      'H': 'Q',
                      'I': 'R',
                      'J': 'S',
                      'K': 'T'}

    app = xw.App(visible=False)
    wb = xw.Book(file_path)
    sheet = wb.sheets[0]

    # clear_colors(sheet)
    start_row = 3
    last_row = sheet.used_range.rows.count

    # Iterate through the rows starting from the specified row until the last row
    for i in range(start_row, last_row + 1):
        # Iterate through the specified columns for comparison
        for col_45, col_15 in column_mapping.items():
            # Get the values for comparison
            value_45 = sheet.range((i, sheet.range(col_45 + '1').column)).value
            value_15 = sheet.range((i, sheet.range(col_15 + '1').column)).value

            if value_45 == value_15:
                sheet.range((i, sheet.range(col_45 + '1').column)).color = (255, 255, 0)
                sheet.range((i, sheet.range(col_15 + '1').column)).color = (255, 255, 0)

    print("Matching the fib levels with 45 and 15 days is complete.")
    wb.save('csv_files/merged_data_and_highlighted_with_ltp.xlsx')
    wb.close()
    app.quit()


latest_ltp = get_latest_ltp()
merge_and_add_ltp()
new_highlight_matching_fib_levels()