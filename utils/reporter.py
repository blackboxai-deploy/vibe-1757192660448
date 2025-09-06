from database.database import SessionLocal
from database.models import Apartment, Contact, Communication
from communication.email_client import EmailClient
from utils.logger import get_logger
from datetime import datetime, timedelta

class Reporter:
    def __init__(self):
        self.db_session = SessionLocal()
        self.email_client = EmailClient()
        self.logger = get_logger(self.__class__.__name__)

    def generate_report(self):
        self.logger.info("Generating daily report...")
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        apartments_scraped = self.db_session.query(Apartment).filter(
            Apartment.scraped_at >= yesterday
        ).count()

        contacts_made = self.db_session.query(Contact).filter(
            Contact.created_at >= yesterday
        ).count()

        communications_sent = self.db_session.query(Communication).filter(
            Communication.timestamp >= yesterday
        ).count()

        report_body = f"""
        Daily Report - {today}

        Apartments Scraped: {apartments_scraped}
        Contacts Made: {contacts_made}
        Communications Sent: {communications_sent}
        """

        self.email_client.send_email("your_email@example.com", f"Daily Report - {today}", report_body)
