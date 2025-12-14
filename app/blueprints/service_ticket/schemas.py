from app.extensions import ma
from app.models import ServiceTicket

class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True
    
ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)