from .seloger import SelogerScraper
from .leboncoin import LeboncoinScraper
from .pap import PapScraper
from .logicimmo import LogicimmoScraper
from config.config import get_config

def run_scrapers():
    config = get_config()
    search_criteria = config['search_criteria']

    scrapers = [
        SelogerScraper(search_criteria),
        LeboncoinScraper(search_criteria),
        PapScraper(search_criteria),
        LogicimmoScraper(search_criteria)
    ]

from communication.email_client import EmailClient
from database.database import SessionLocal
from database.models import Contact, Communication, Apartment

    for scraper in scrapers:
        apartments = scraper.scrape()
        for apartment_data in apartments:
            db_session = SessionLocal()
            # Check for duplicates
            existing_apartment = db_session.query(Apartment).filter_by(url=apartment_data['url']).first()
            if not existing_apartment:
                # Create new apartment and agency
                # ... (logic to create apartment and agency)

                # Create contact and send email
                contact = Contact(
                    name=apartment_data['agency_name'], 
                    email=apartment_data['agency_email'], 
                    phone=apartment_data['agency_phone']
                )
                db_session.add(contact)
                db_session.commit()

                email_client = EmailClient()
                email_client.send_email(contact.email, "Apartment Inquiry", "... (email content) ...")

                communication = Communication(
                    apartment_id=apartment.id,
                    contact_id=contact.id,
                    type='email',
                    content="... (email content) ..."
                )
                db_session.add(communication)
                db_session.commit()
