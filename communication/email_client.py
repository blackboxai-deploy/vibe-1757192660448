import smtplib
from email.mime.text import MIMEText
from config.config import get_config
from utils.logger import get_logger

class EmailClient:
    def __init__(self):
        self.config = get_config()['email']
        self.logger = get_logger(self.__class__.__name__)

    def send_email(self, to_email, subject, body):
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.config['smtp_user']
            msg['To'] = to_email

            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['smtp_user'], self.config['smtp_password'])
                server.send_message(msg)
            self.logger.info(f"Email sent to {to_email}")
        except Exception as e:
            self.logger.error(f"Error sending email to {to_email}: {e}")
