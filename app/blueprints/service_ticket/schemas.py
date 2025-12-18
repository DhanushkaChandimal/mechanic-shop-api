from app.extensions import ma
from app.models import ServiceTicket, ServiceItems
from marshmallow import fields

class ServiceItemsSchema(ma.SQLAlchemyAutoSchema):
    item = fields.Nested('ItemSchema', dump_only=True)
    
    class Meta:
        model = ServiceItems
        include_fk = True

class TicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested('MechanicSchema', many=True, dump_only=True)
    service_items = fields.Nested(ServiceItemsSchema, many=True, dump_only=True)
    
    class Meta:
        model = ServiceTicket
        include_relationships = True

class EditTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")
    
ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)
edit_ticket_schema = EditTicketSchema()
