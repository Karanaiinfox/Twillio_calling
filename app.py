# app.py
from flask import Flask, render_template, request, redirect, url_for
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(account_sid, auth_token)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to initiate the call via Twilio
@app.route('/make_call', methods=['POST'])
def make_call():
    to_number = request.form.get('to_number')
    code = request.form.get('country_code')
    to_number=f"{code}{to_number}"
    custom_message = request.form.get('message', 'Hello from Flask and Twilio!')

    # Make an outbound call using Twilio
    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        twiml=f'<Response><Say>{custom_message}</Say></Response>'
        # record=True,
        # transcribe=True,
        # transcribe_callback=url_for('handle_transcription', _external=True)
    )

    return render_template('call_status.html', call_sid=call.sid, to_number=to_number)

# Webhook for incoming calls
@app.route('/incoming_call', methods=['POST'])
def incoming_call():
    response = VoiceResponse()
    response.say("Hello, this is an automated response from Flask and Twilio. Goodbye!")
    return str(response)

# Handle transcription of recorded calls
@app.route('/handle_transcription', methods=['POST'])
def handle_transcription():
    transcription_text = request.form.get('TranscriptionText')
    call_sid = request.form.get('CallSid')

    # Print transcription or log it for later use
    print(f"Transcription for Call SID {call_sid}: {transcription_text}")
    
    return ('', 204)  # Respond with no content

if __name__ == '__main__':
    app.run(debug=True)