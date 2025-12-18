from app.extensions import ma
from app.models import ServiceTicket, ServiceItems, Item
from marshmallow import fields

class ItemInTicketSchema(ma.Schema):
    id = fields.Int(attribute='item.id')
    name = fields.Str(attribute='item.name')
    price = fields.Float(attribute='item.price')
    quantity = fields.Int()

class TicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested('MechanicSchema', many=True, dump_only=True)
    items = fields.Nested(ItemInTicketSchema, many=True, attribute='service_items', dump_only=True)
    customer_id = fields.Int()
    
    class Meta:
        model = ServiceTicket

class EditTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")
    
ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)
edit_ticket_schema = EditTicketSchema()
