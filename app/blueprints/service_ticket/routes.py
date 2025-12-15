from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from .schemas import ticket_schema, tickets_schema, edit_ticket_schema
from app.models import ServiceTicket, Mechanic, Customer, db
from . import tickets_bp
from app.extensions import limiter, cache
from app.utils.util import token_required

# CREATE SERVICE TICKET
@tickets_bp.route("/", methods=['POST'])
@limiter.limit("30 per hour")
def create_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer = db.session.get(Customer, ticket_data.get('customer_id'))
    if not customer:
        return jsonify({"error": "Customer not found. Please provide a valid customer_id."}), 404
    
    new_ticket = ServiceTicket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201

#GET ALL SERVICE TICKETS
@tickets_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()

    return tickets_schema.jsonify(tickets)

#GET SPECIFIC SERVICE TICKET
@tickets_bp.route("/<int:ticket_id>", methods=['GET'])
def get_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)

    if ticket:
        return ticket_schema.jsonify(ticket), 200
    return jsonify({"error": "Ticket not found."}), 404

#GET SERVICE TICKETS BY CUSTOMER
@tickets_bp.route("/my-tickets", methods=['GET'])
@token_required
def get_tickets_by_customer(customer_id):
    query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id) 
    tickets = db.session.execute(query).scalars().all()

    if tickets:
        return tickets_schema.jsonify(tickets), 200
    return jsonify({"error": "No tickets associated with you"}), 404

#DELETE SPECIFIC SERVICE TICKET
@tickets_bp.route("/<int:ticket_id>", methods=['DELETE'])
@limiter.limit("2 per hour")
def delete_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)

    if not ticket:
        return jsonify({"error": "Ticket not found."}), 404
    
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f'Ticket id: {ticket_id}, successfully deleted.'}), 200

@tickets_bp.route("/<int:ticket_id>/edit", methods=['PUT'])
def edit_ticket(ticket_id):
    try:
        ticket_edits = edit_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(ServiceTicket).where(ServiceTicket.id == ticket_id) 
    ticket = db.session.execute(query).scalars().first()
    
    for mechanic_id in ticket_edits['add_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()
        
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mechanic_id in ticket_edits['remove_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()
        
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()
    return ticket_schema.jsonify(ticket)
