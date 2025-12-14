from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from .schemas import ticket_schema, tickets_schema
from app.models import ServiceTicket, db
from . import tickets_bp

# CREATE SERVICE TICKET
@tickets_bp.route("/", methods=['POST'])
def create_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_ticket = ServiceTicket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201

#GET ALL SERVICE TICKETS
@tickets_bp.route("/", methods=['GET'])
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

#UPDATE SPECIFIC SERVICE TICKET
@tickets_bp.route("/<int:ticket_id>", methods=['PUT'])
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
def delete_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)

    if not ticket:
        return jsonify({"error": "Ticket not found."}), 404
    
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f'Ticket id: {ticket_id}, successfully deleted.'}), 200
