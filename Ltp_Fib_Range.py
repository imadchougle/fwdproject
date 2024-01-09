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

    for range_name, bounds in fibonacci_ranges.items():
        lower, upper = bounds
        if lower <= stock_price <= upper:
            return f"For {stock_name}, the stock price {stock_price} is in {range_name}"

    return f"For {stock_name}, the stock price {stock_price} is not in any Fibonacci range"


stocks = ["XYZ", "ABC", "123", "PNB"]
stock_prices = [620, 910, 450, 97.5]

fib_levels_stocks = [
    (500, 550, 580, 600, 620, 650, 680, 700, 750),
    (700, 750, 780, 800, 820, 850, 880, 900, 950),
    (400, 450, 480, 500, 520, 550, 580, 600, 650),
    (60, 90, 100, 120, 100, 90, 50, 90, 50)
]

for i in range(len(stocks)):
    result = find_fibonacci_range(stocks[i],
                                  stock_prices[i],
                                  fib_levels_stocks[i])
    print(result)