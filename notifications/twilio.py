# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "AC4a51dde40cbbe0cb0d4d648f7372f003"
auth_token = "744e8a1392f370bf9bfe49a791b2b17f"
verify_sid = "VAdbd2c104eae5f63ddd435ac57cd78b42"
verified_number = "+918355921551"

client = Client(account_sid, auth_token)

verification = client.verify.v2.services(verify_sid) \
  .verifications \
  .create(to=verified_number, channel="sms")
print(verification.status)

otp_code = input("Please enter the OTP:")

verification_check = client.verify.v2.services(verify_sid) \
  .verification_checks \
  .create(to=verified_number, code=otp_code)
print(verification_check.status)