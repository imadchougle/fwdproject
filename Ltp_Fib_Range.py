import xlwings as xw
from get_LTP_from_here import get_latest_ltp
from utils import scripts
from get_fib_prices_from_here import d45_fib_prices, d15_fib_prices


def adding_ltp_column_and_data():
    file_path = 'csv_files/merged_data_with_ltp.xlsx'
    wb = xw.Book(file_path)
    sheet = wb.sheets[0]

    sheet.range('C:C').api.Insert(Shift=-4161)  # -4161 corresponds to shifting to the right
    sheet.range('C2').value = '45 Days'

    sheet.range('D:D').api.Insert(Shift=-4161)  # -4161 corresponds to shifting to the right
    sheet.range('D2').value = '15 Days'

    cell_to_add = 'C3'
    sheet.range(cell_to_add).options(transpose=True).value = new_result_45days

    cell_to_add = 'D3'
    sheet.range(cell_to_add).options(transpose=True).value = new_result_15days

    cell_to_add = 'B3'
    sheet.range(cell_to_add).options(transpose=True).value = stock_prices

    wb.save('csv_files/merged_data_with_ltp_and_Range.xlsx')
    wb.close()


def find_fibonacci_range(stock_name, stock_price, fib_levels):
    fibonacci_ranges = {
        '0 - 0.236': (fib_levels[0], fib_levels[1]),
        '0.236 - 0.382': (fib_levels[1], fib_levels[2]),
        '0.382 - 0.5': (fib_levels[2], fib_levels[3]),
        '0.5 - 0.618': (fib_levels[3], fib_levels[4]),
        '0.618 - 0.786': (fib_levels[4], fib_levels[5]),
        '0.786 - 1': (fib_levels[5], fib_levels[6]),
        '1 - 1.236': (fib_levels[6], fib_levels[7]),
        '1.236 - 1.618': (fib_levels[7], fib_levels[8]),
        '1.618 + ': (fib_levels[8], float('inf'))
    }

    result_range = []  # Initialize the list for each stock
    for range_name, bounds in fibonacci_ranges.items():
        lower, upper = bounds
        if lower <= stock_price <= upper:
            result_range.append(range_name)

    # If the stock doesn't fall into any range, add a placeholder value
    if not result_range:
        result_range.append('Less than 0')

    return result_range


if __name__ == "__main__":
    latest_ltp = get_latest_ltp()
    result_range_45days = []
    result_range_15days = []
    stocks = scripts
    stock_prices = latest_ltp

    fib_levels_of_45_days = d45_fib_prices
    fib_levels_of_15_days = d15_fib_prices

    for i in range(len(stocks)):
        result_of_45days = find_fibonacci_range(stocks[i], stock_prices[i], fib_levels_of_45_days[i])
        result_range_45days += result_of_45days  # Concatenate the result for each stock

        result_of_15days = find_fibonacci_range(stocks[i], stock_prices[i], fib_levels_of_15_days[i])
        result_range_15days += result_of_15days  # Concatenate the result for each stock

    new_result_45days = result_range_45days
    new_result_15days = result_range_15days

    adding_ltp_column_and_data()
