from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

ticket_mechanic = db.Table(
    'ticket_mechanic',
    Base.metadata,
    db.Column('ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

class Customer(Base):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(254), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(25))

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer')

class ServiceTicket(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(25), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date)
    service_description: Mapped[str] = mapped_column(db.String(360), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=ticket_mechanic, back_populates='service_tickets')
    
class Mechanic(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(254), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(db.String(360), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(25))
    salary: Mapped[float] = mapped_column(db.Numeric(10, 2))
    
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=ticket_mechanic, back_populates='mechanics')