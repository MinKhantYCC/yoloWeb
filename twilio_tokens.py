# Download the helper library from https://www.twilio.com/docs/python/install
# ORIFzZF0D7gNZW37aXImKBwBoL9xL2GB
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

token = client.tokens.create()

print(token.username)
print(token.account_sid)
print(token.date_created)
print(token.date_updated)
print(token.password)
print(token.ttl)
print(token.ice_servers)
