from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from .schemas import ticket_schema, tickets_schema
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
    query =select(ServiceTicket).where(ServiceTicket.customer_id == customer_id) 
    tickets = db.session.execute(query).scalars().all()

    if tickets:
        return tickets_schema.jsonify(tickets), 200
    return jsonify({"error": "No tickets associated with you"}), 404

#UPDATE SPECIFIC SERVICE TICKET
@tickets_bp.route("/<int:ticket_id>", methods=['PUT'])
@limiter.limit("30 per hour")
def update_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)

    if not ticket:
        return jsonify({"error": "Ticket not found."}), 404
    
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in ticket_data.items():
        setattr(ticket, key, value)

    db.session.commit()
    return ticket_schema.jsonify(ticket), 200

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

# ASSIGN MECHANIC TO SERVICE TICKET
@tickets_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=['PUT'])
@limiter.limit("150 per hour")
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    if mechanic in ticket.mechanics:
        return jsonify({"error": "Mechanic already assigned to this ticket."}), 400
    
    ticket.mechanics.append(mechanic)
    db.session.commit()
    
    return jsonify({"message": f'Mechanic {mechanic_id}, successfully assigned to service ticket {ticket_id}.'}), 200

# REMOVE MECHANIC FROM SERVICE TICKET
@tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
@limiter.limit("75 per hour")
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    if mechanic not in ticket.mechanics:
        return jsonify({"error": "Mechanic is not assigned to this ticket."}), 400
    
    ticket.mechanics.remove(mechanic)
    db.session.commit()
    
    return jsonify({"message": f'Mechanic {mechanic_id}, successfully removed from service ticket {ticket_id}.'}), 200
