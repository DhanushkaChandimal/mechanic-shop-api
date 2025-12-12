from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/mechanic_shop_db'

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Customer(Base):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(254), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(25))

class ServiceTicket(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(25), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date)
    service_description: Mapped[str] = mapped_column(db.String(360), nullable=False)
    
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))
    
class Mechanic(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(254), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(db.String(360), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(25))
    salary: Mapped[float] = mapped_column(db.Numeric(10, 2))

with app.app_context():
    db.create_all()
app.run(debug=True)