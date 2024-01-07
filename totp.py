import pyotp

totp = pyotp.TOTP("NHIMW7WPKRT2JTOCMKVBQA2A5OPMOEXL")

otp_code = totp.now()
print(f'Generated TOTP code: {otp_code}')