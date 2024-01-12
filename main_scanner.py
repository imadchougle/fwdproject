import xlwings as xw
from utils import *
from get_LTP_from_here import *
import pandas as pd


def merger():
    df_45_days = pd.read_csv('csv_files/D45_cycle.csv', index_col='stock')
    df_15_days = pd.read_csv('csv_files/D15_cycle.csv', index_col='stock')

    merged_df = pd.concat([df_45_days, df_15_days],
                          axis=1,
                          keys=['45 days', '15 days'])

    wb = xw.Book()

    sheet = wb.sheets['Sheet1']
    sheet.range('A1').value = merged_df

    wb.save('csv_files/merged_data_without_LTP.xlsx')

    wb.close()
    print("Done Merging it")


def adding_ltp_column_and_ltp():
    file_path = 'csv_files/merged_data_without_LTP.xlsx'
    wb = xw.Book(file_path)
    sheet = wb.sheets[0]

    sheet.range('B:B').api.Insert(Shift=-4161)  # -4161 corresponds to shifting to the right
    sheet.range('B2').value = 'ltp'

    cell_to_add = 'B3'
    sheet.range(cell_to_add).options(transpose=True).value = latest_ltp

    wb.save('csv_files/merged_data_with_ltp.xlsx')
    wb.close()
    print("Done Adding 'ltp' Column and added the Last Traded Price")


def clear_colors(sheet):
    red_color = (255, 0, 0)
    used_range = sheet.used_range
    for cell in used_range:
        if cell.color == red_color:
            cell.color = None


def highlight_matching_ltp_with_fib_level_price(file_path):
    app = xw.App(visible=False)
    wb = xw.Book(file_path)
    sheet = wb.sheets[0]
    total_rows = sheet.range((2, 1)).end('down').row

    clear_colors(sheet)

    # here we Iterate through the rows starting from the third row
    for i in range(3, total_rows + 1):
        # Get the LTP value in the current row
        ltp = sheet.range((i, 2)).value

        # Iterate through the cells starting from the 3rd column (index 2)
        for j in range(3, sheet.range((i, 1)).end('right').column + 1):
            # Get the fib level value in the current column
            fib_level = sheet.range((i, j)).value

            if ltp == fib_level:
                sheet.range((i, 2)).color = (255, 0, 0)
                sheet.range((i, j)).color = (255, 0, 0)

    print("Done with matching the Ltp with fib prices")
    wb.save()
    wb.close()
    app.quit()


def highlight_matching_fib_levels(file_path):
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
    wb.save()
    wb.close()
    app.quit()


if __name__ == "__main__":
    #merger()

    #latest_ltp = get_latest_ltp()
    #adding_ltp_column_and_ltp()
    #highlight_matching_ltp_with_fib_level_price('csv_files/merged_data_with_ltp.xlsx')

    highlight_matching_fib_levels('csv_files/merged_data_with_ltp.xlsx')