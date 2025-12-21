from app import create_app
from app.models import db, Mechanic
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanic(name="test_mechanic", email="test_mechanic@email.com", address="test_mechanic_address", phone="555-555-5555", salary=200)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Test Mechanic",
            "email": "testmech@email.com",
           	"address": "Test address",
           	"phone": "555-555-5555",
            "salary": 300
        }
        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Test Mechanic")

    def test_invalid_mechanic_creation(self):
        mechanic_payload = {
            "name": "Test Mechanic",
            "email": "testmech@email.com",
           	"address": "Test address",
            "salary": 300
        }
        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['phone'], ['Missing data for required field.'])

    def test_get_all_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_mechanic')
        self.assertEqual(response.json[0]['email'], 'test_mechanic@email.com')
        self.assertEqual(response.json[0]['id'], 1)

    def test_get_specific_mechanic(self):
        response = self.client.get('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'test_mechanic')
        self.assertEqual(response.json['email'], 'test_mechanic@email.com')
        self.assertEqual(response.json['id'], 1)

    def test_update_mechanic(self):
        update_payload = {
            "name": "Test Mechanic Updated",
            "email": "testmech@email.com",
           	"address": "Test address updated",
           	"phone": "555-555-5555",
            "salary": 300
        }
        response = self.client.put('/mechanics/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test Mechanic Updated')
        self.assertEqual(response.json['address'], 'Test address updated')

    def test_delete_mechanic(self):
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Mechanic id: 1, successfully deleted.')
