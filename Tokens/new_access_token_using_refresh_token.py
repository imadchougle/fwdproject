import requests
import json
import hashlib


apicredfile = open('C:/Users/imadc/PycharmProjects/fwdproject/UserCred.json')
UserCred = json.load(apicredfile)

refresh_token_url = "https://api-t1.fyers.in/api/v3/validate-refresh-token"


app_id = UserCred["client_id"]
app_secret = UserCred["secret_id"]
pin = UserCred["pin"]

app_id_hash = hashlib.sha256(f"{app_id}:{app_secret}".encode()).hexdigest()

with open('refresh_token.txt', 'r') as file:
    refresh_token = file.read().strip()

data = {
    "grant_type": "refresh_token",
    "appIdHash": app_id_hash,
    "refresh_token": refresh_token,
    "pin": pin
}

response = requests.post(refresh_token_url,
                         json=data,
                         headers={"Content-Type": "application/json"})

response_data = response.json()

if response_data.get('s') == 'ok':
    new_access_token = response_data.get('access_token')
    print("New Access Token:", new_access_token)
else:
    print("Error:", response_data.get('message'))