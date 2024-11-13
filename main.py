# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC5299bc8699e481c78a016b209aa0c57f'
auth_token = '045050af6fdc2c0a151153f75afdc86d'
client = Client(account_sid, auth_token)

custom_message="  Hello, This is a test message from Twilio. Please ignore this message. Thank you.  "
twiml_url = f"http://twimlets.com/echo?Twiml=<Response><Say>{custom_message}</Say></Response>"
call = client.calls.create(
    # url=twiml_url,
    twiml=f'<Response><Say>{custom_message}</Say></Response>',
    to="+918219383324",
    from_="+13204039182",
    record=True,
    transcribe=True,
    transcribe_callback='/handle_transcription' 
)
print(call)


