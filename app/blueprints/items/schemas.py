from app.extensions import ma
from app.models import Item

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
    
item_schema =ItemSchema()
items_schema = ItemSchema(many=True)
