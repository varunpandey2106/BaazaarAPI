from twilio.rest import Client
from django.conf import settings

def send_sms_notification(user):
    # Initialize Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Define the message body and recipient phone number
    message_body = f"Hello {user.username}, HALO/OHAAYO gurlfrendo/biwi san. Welcome to varun's heart, you have been logged in. COMPUTER SCIENCE RIZZ ;)"
    to_phone_number = "+919821110201"  # Replace with the user's phone number

    # Send the SMS
    message = client.messages.create(
        body=message_body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_phone_number,
    )

    return message.sid