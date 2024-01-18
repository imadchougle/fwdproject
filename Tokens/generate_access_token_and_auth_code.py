from fyers_apiv3 import fyersModel
import json

apicredfile = open('C:/Users/imadc/PycharmProjects/fwdproject/UserCred.json')
UserCred = json.load(apicredfile)

client_id = UserCred["client_id"]
secret_key = UserCred["secret_id"]
redirect_uri = UserCred["redirect_uri"]
response_type = UserCred["response_type"]
state = UserCred["state"]
grant_type = UserCred["grant_type"]

#session model
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type
)

# from this we will Generate the auth code using the session model
response = session.generate_authcode()

print(response)

# url = session.generate_authcode()
# print(url)

auth_code = input("Enter auth code: ")

session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type,
    grant_type=grant_type
)


session.set_token(auth_code)
token_response = session.generate_token()
print(token_response)

with open('access_token.txt', 'w') as access_token_file:
    access_token_file.write(token_response['access_token'])

with open('refresh_token.txt', 'w') as refresh_token_file:
    refresh_token_file.write(token_response['refresh_token'])

