from fyers_apiv3 import fyersModel
import json

'''
Run this script after refreshing the new Access Token before starting anything, 
to check if everything is correct if you get the LTP of SBI 
then You can proceed ahead
'''

apicredfile = open('UserCred.json')
UserCred = json.load(apicredfile)

with open('Tokens/access_token.txt', 'r') as file:
    token = file.read().strip()

client_id = UserCred["client_id"]

fyers = fyersModel.FyersModel(client_id=client_id,
                                is_async=False,
                                token=token
                                )


data = {
        "symbols": "NSE:SBIN-EQ"
    }

response = fyers.quotes(data=data)
ltp = response.get("d", [])[0].get("v", {}).get("lp")

print(f"Last Traded Price of SBI = {ltp}")
