from app import create_app
from app.models import db, Item
import unittest

class TestItem(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.item = Item(name="test_item", price=200)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.item)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_item(self):
        item_payload = {
            "name": "Test Item",
            "price": 100
        }
        response = self.client.post('/inventory/', json=item_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Test Item")
        self.assertEqual(response.json['price'], 100)

    def test_invalid_item_creation(self):
        item_payload = {
            "name": "Test Item"
        }
        response = self.client.post('/inventory/', json=item_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['price'], ['Missing data for required field.'])

    def test_get_all_items(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_item')
        self.assertEqual(response.json[0]['price'], 200)
        self.assertEqual(response.json[0]['id'], 1)

    def test_get_specific_item(self):
        response = self.client.get('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'test_item')
        self.assertEqual(response.json['price'], 200)
        self.assertEqual(response.json['id'], 1)

    def test_update_item(self):
        update_payload = {
            "name": "Test Item Updated",
            "price": 300
        }
        response = self.client.put('/inventory/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test Item Updated')

    def test_delete_item(self):
        response = self.client.delete('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Item with id: 1, successfully deleted.')
