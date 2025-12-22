from app import create_app
from app.models import db, ServiceTicket, Customer, Mechanic, Item
import unittest
from datetime import date
from app.utils.util import encode_token

class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customer(name="test_user", email="test@email.com", phone="555-555-5555", password='test')
        self.mechanic1 = Mechanic(name="test_mechanic_1", email="test_mechanic_1@email.com", address="test_mechanic_address_1", phone="111-111-1111", salary=100)
        self.item = Item(name="test_item", price=200)
        self.ticket = ServiceTicket(vin="111111111111111", service_date=date(2025, 12, 21), service_description="test_ticket_description", customer_id=1)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.add(self.mechanic1)
            db.session.add(self.item)
            db.session.add(self.ticket)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def test_create_ticket(self):
        ticket_payload = {
            "vin": "12345678901234",
            "service_date": "2025-12-21",
           	"service_description": "Test service description",
            "customer_id": 1
        }
        response = self.client.post('/service-tickets/', json=ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['vin'], "12345678901234")

    def test_invalid_ticket_creation(self):
        ticket_payload = {
            "vin": "12345678901234",
            "service_date": "2025-12-21",
            "customer_id": 1
        }
        response = self.client.post('/service-tickets/', json=ticket_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['service_description'], ['Missing data for required field.'])

    def test_get_all_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['vin'], '111111111111111')
        self.assertEqual(response.json[0]['service_date'], '2025-12-21')
        self.assertEqual(response.json[0]['customer_id'], 1)

    def test_get_specific_ticket(self):
        response = self.client.get('/service-tickets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['vin'], '111111111111111')
        self.assertEqual(response.json['service_date'], '2025-12-21')
        self.assertEqual(response.json['customer_id'], 1)
        self.assertEqual(response.json['id'], 1)

    def test_get_tickets_for_specific_customer(self):
        headers = {'Authorization': 'Bearer ' + self.token}
        response = self.client.get('/service-tickets/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['vin'], '111111111111111')
        self.assertEqual(response.json[0]['service_date'], '2025-12-21')
        self.assertEqual(response.json[0]['customer_id'], 1)
        self.assertEqual(response.json[0]['id'], 1)

    def test_delete_ticket(self):
        response = self.client.delete('/service-tickets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Ticket id: 1, successfully deleted.')

    def test_assign_mechanics_for_ticket(self):
        ticket_payload = {
            "add_mechanic_ids": [1],
            "remove_mechanic_ids": []
        }
        response = self.client.put('/service-tickets/1/edit', json=ticket_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['vin'], "111111111111111")
        self.assertEqual(response.json['service_description'], "test_ticket_description")
        self.assertEqual(response.json['mechanics'][0]['id'], 1)
        self.assertEqual(response.json['mechanics'][0]['name'], 'test_mechanic_1')

    def test_remove_mechanics_from_ticket(self):
        add_payload = {
            "add_mechanic_ids": [1],
            "remove_mechanic_ids": []
        }
        response = self.client.put('/service-tickets/1/edit', json=add_payload)
        self.assertEqual(response.json['mechanics'][0]['id'], 1)
        
        remove_payload = {
            "add_mechanic_ids": [],
            "remove_mechanic_ids": [1]
        }
        response = self.client.put('/service-tickets/1/edit', json=remove_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['vin'], "111111111111111")
        self.assertEqual(response.json['service_description'], "test_ticket_description")
        self.assertEqual(len(response.json['mechanics']), 0)

    def test_add_part_for_ticket(self):
        response = self.client.put('/service-tickets/add-part/1/to-ticket/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['vin'], "111111111111111")
        self.assertEqual(response.json['service_description'], "test_ticket_description")
        self.assertEqual(len(response.json['items']), 1)
        self.assertEqual(response.json['items'][0]['id'], 1)
        self.assertEqual(response.json['items'][0]['name'], 'test_item')
