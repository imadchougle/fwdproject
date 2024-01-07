from datetime import date, timedelta

current_date = date.today()

day = current_date.day

current_date = date.today()

previous_month = current_date.replace(day=1) - timedelta(days=1)


if day < 15:
    end_date = previous_month
    n = int(input("Enter how many last days you need"))
    start_date = end_date - timedelta(days=n)

    print("start date: ", start_date)
    print("end date: ", end_date)
else:
    first_day_of_next_month = date(current_date.year, current_date.month, 1) + timedelta(days=32)
    end_date = first_day_of_next_month.replace(day=1) - timedelta(days=1)

    n = int(input("Enter how many last days you need"))
    start_date = end_date - timedelta(days=n)

    print("start date: ", start_date)
    print("end date: ", end_date)