from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    address = Column(String)
    price = Column(Float)
    size = Column(Float)
    description = Column(String)
    scraped_at = Column(DateTime)
    agency_id = Column(Integer, ForeignKey('agencies.id'))
    agency = relationship('Agency', back_populates='apartments')
    communications = relationship('Communication', back_populates='apartment')

class Agency(Base):
    __tablename__ = 'agencies'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    phone = Column(String)
    email = Column(String)
    apartments = relationship('Apartment', back_populates='agency')
    contacts = relationship('Contact', back_populates='agency')

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    status = Column(String, default='new')
    agency_id = Column(Integer, ForeignKey('agencies.id'))
    agency = relationship('Agency', back_populates='contacts')
    communications = relationship('Communication', back_populates='contact')

class Communication(Base):
    __tablename__ = 'communications'

    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey('apartments.id'))
    apartment = relationship('Apartment', back_populates='communications')
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    contact = relationship('Contact', back_populates='communications')
    timestamp = Column(DateTime)
    type = Column(String)  # 'email' or 'call'
    content = Column(String)
    responded = Column(Boolean, default=False)
