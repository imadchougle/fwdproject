from fyers_apiv3 import fyersModel
import json
import csv

apicredfile = open('UserCred.json')
UserCred = json.load(apicredfile)


file_path = 'csv_files/merged_data_without_LTP.csv'


with open('Tokens/access_token.txt', 'r') as file:
    token = file.read().strip()


client_id = UserCred["client_id"]


fyers = fyersModel.FyersModel(client_id=client_id,
                              is_async=False,
                              token=token
                              )
stock_ltp = []

with open(file_path, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    header.insert(1, 'ltp')

    rows = [row for row in reader]
    for i, row in enumerate(rows):
        script = row[0]  # Assuming the script is in the first column
        data = {"symbols": "NSE:" + script + "-EQ"}
        response = fyers.quotes(data=data)
        ltp = response.get("d", [])[0].get("v", {}).get("lp") if response else None

        # Update 'ltp' value in the row if it is there
        if ltp is not None:
            row.insert(1, ltp)
        else:
            row.insert(1, '')  # here we handle the case where 'ltp' is not available

# Writing the updated data to a new CSV file
output_file_path = 'csv_files/Combined_with_LTP.csv'
with open(output_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows)

print(f'Updated CSV file saved at: {output_file_path}')