from twilio.rest import Client
from config.config import get_config
from utils.logger import get_logger

class PhoneClient:
    def __init__(self):
        self.config = get_config()['api_keys']
        self.client = Client(self.config['twilio_sid'], self.config['twilio_auth_token'])
        self.logger = get_logger(self.__class__.__name__)

    def make_call(self, to_number, message):
        try:
            call = self.client.calls.create(
                twiml=f'<Response><Say>{message}</Say></Response>',
                to=to_number,
                from_=self.config['twilio_phone_number']
            )
            self.logger.info(f"Call made to {to_number}: {call.sid}")
        except Exception as e:
            self.logger.error(f"Error making call to {to_number}: {e}")
