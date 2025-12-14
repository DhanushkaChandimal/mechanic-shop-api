from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy import select

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/mechanic_shop_db'

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
db.init_app(app)
ma.init_app(app)

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

# ==========SCHEMAS==========
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
    
customer_schema =CustomerSchema()
customers_schema = CustomerSchema(many=True)

# ==========ROUTES==========

# CREATE CUSTOMER
@app.route("/customers", methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    
    if(existing_customer): return jsonify({"error": "Email already used"}), 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

#GET ALL CUSTOMERS
@app.route("/customers", methods=['GET'])
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()

    return customers_schema.jsonify(customers)

#GET SPECIFIC CUSTOMER
@app.route("/customers/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404

# with app.app_context():
#     db.create_all()
app.run(debug=True)