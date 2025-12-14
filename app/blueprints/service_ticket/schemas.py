from app.extensions import ma
from app.models import ServiceTicket
from marshmallow import fields

class TicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested('MechanicSchema', many=True)
    
    class Meta:
        model = ServiceTicket
        include_fk = True
        include_relationships = True
    
ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)