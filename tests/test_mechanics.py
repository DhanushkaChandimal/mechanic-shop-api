from app import create_app
from app.models import db, Mechanic, ServiceTicket, Customer
import unittest
from datetime import date

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

    def test_get_most_worked_mechanics(self):
        mechanic2 = Mechanic(name="mechanic_2", email="mechanic2@email.com", address="address_2", phone="555-555-5556", salary=300)
        mechanic3 = Mechanic(name="mechanic_3", email="mechanic3@email.com", address="address_3", phone="555-555-5557", salary=400)
        
        customer = Customer(name="test_customer", email="customer@email.com", phone="555-555-5558", password="test")
        
        ticket1 = ServiceTicket(vin="VIN111111111111", service_date=date(2025, 12, 21), service_description="Service 1", customer_id=1)
        ticket2 = ServiceTicket(vin="VIN222222222222", service_date=date(2025, 12, 22), service_description="Service 2", customer_id=1)
        ticket3 = ServiceTicket(vin="VIN333333333333", service_date=date(2025, 12, 23), service_description="Service 3", customer_id=1)
        
        with self.app.app_context():
            db.session.add(mechanic2)
            db.session.add(mechanic3)
            db.session.add(customer)
            db.session.commit()

            db.session.add(ticket1)
            db.session.add(ticket2)
            db.session.add(ticket3)
            db.session.commit()

            ticket1.mechanics.append(self.mechanic)
            ticket2.mechanics.append(self.mechanic)
            ticket3.mechanics.append(self.mechanic)
            
            ticket1.mechanics.append(mechanic2)
            
            ticket2.mechanics.append(mechanic3)
            ticket3.mechanics.append(mechanic3)
            
            db.session.commit()
        
        response = self.client.get('/mechanics/most-worked')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(response.json[0]['name'], 'test_mechanic')
        self.assertEqual(response.json[1]['name'], 'mechanic_3')
        self.assertEqual(response.json[2]['name'], 'mechanic_2')
