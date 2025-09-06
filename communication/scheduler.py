from apscheduler.schedulers.background import BackgroundScheduler
from database.database import SessionLocal
from database.models import Contact, Communication
from communication.email_client import EmailClient
from communication.phone_client import PhoneClient
from utils.logger import get_logger
from datetime import datetime, timedelta

class FollowUpScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.db_session = SessionLocal()
        self.email_client = EmailClient()
        self.phone_client = PhoneClient()
        self.logger = get_logger(self.__class__.__name__)

    def start(self):
        self.scheduler.add_job(self.follow_up, 'interval', hours=1)
        self.scheduler.start()
        self.logger.info("Follow-up scheduler started.")

    def follow_up(self):
        self.logger.info("Running follow-up job...")
        contacts_to_follow_up = self.db_session.query(Contact).filter(
            Contact.status == 'contacted'
        ).all()

        for contact in contacts_to_follow_up:
            last_communication = self.db_session.query(Communication).filter(
                Communication.contact_id == contact.id
            ).order_by(Communication.timestamp.desc()).first()

            if last_communication and last_communication.timestamp < datetime.now() - timedelta(days=1):
                self.logger.info(f"Following up with {contact.name} ({contact.email})")
                # Send a follow-up email
                self.email_client.send_email(contact.email, "Relance concernant votre appartement", "... (follow-up email content) ...")
                # Make a follow-up call
                self.phone_client.make_call(contact.phone, "Bonjour, je vous contacte concernant l'appartement...")

                # Update communication record
                communication = Communication(
                    apartment_id=last_communication.apartment_id,
                    contact_id=contact.id,
                    type='email_follow_up',
                    content="... (follow-up email content) ..."
                )
                self.db_session.add(communication)
                self.db_session.commit()
