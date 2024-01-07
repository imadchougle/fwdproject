import xlwings as xw
import numpy as np

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

    # Iterate through the rows starting from the third row
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

    print("Done with matching the Ltp with fib levels")
    wb.save()
    wb.close()
    app.quit()


highlight_matching_ltp_with_fib_level_price('Combined_with_LTP.xlsx')


def highlight_matching_fib_levels(file_path):
    app = xw.App(visible=False)
    wb = xw.Book(file_path)
    sheet = wb.sheets[0]

    #clear_colors(sheet)
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

    print("Done with matching the fib levels with 45 and 15 days")
    wb.save()
    wb.close()
    app.quit()


#mapping of columns to compare
column_mapping = {'C': 'L', 'D': 'M', 'E': 'N', 'F': 'O', 'G': 'P', 'H': 'Q', 'I': 'R', 'J': 'S', 'K': 'T'}

highlight_matching_fib_levels('Combined_with_LTP.xlsx')