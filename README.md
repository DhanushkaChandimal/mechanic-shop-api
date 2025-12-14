# Mechanic Shop API

A RESTful API for managing a mechanic shop's operations, including customers, mechanics, and service tickets. Built with Flask, SQLAlchemy, and Marshmallow using the Application Factory Pattern.

## Features

- **Customer Management**: Create, read, update, and delete customer records
- **Mechanic Management**: Full CRUD operations for mechanic profiles
- **Service Ticket Management**: Track service requests and repairs
- **Mechanic Assignment**: Assign and remove mechanics to/from service tickets
- **Many-to-Many Relationships**: Multiple mechanics can work on multiple service tickets
- **Data Validation**: Marshmallow schemas for request/response validation
- **Blueprint Architecture**: Modular, scalable application structure

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Marshmallow**: Object serialization/deserialization
- **Flask-SQLAlchemy**: Flask integration with SQLAlchemy
- **Flask-Marshmallow**: Flask integration with Marshmallow
- **MySQL**: Database (configurable)

## Project Structure

```
mechanic-shop-api/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── extensions.py
│   └── blueprints/
│       ├── customers/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       ├── mechanics/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       └── service_ticket/
│           ├── __init__.py
│           ├── routes.py
│           └── schemas.py
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DhanushkaChandimal/mechanic-shop-api.git
   cd "mechanic-shop-api"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**
   - Update `config.py` with your database connection string
   - Uncomment the database creation code in `app.py` (first run only):
   ```python
   with app.app_context():
       db.create_all()
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Customers (`/customers`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/customers/` | Create a new customer |
| GET | `/customers/` | Get all customers |
| GET | `/customers/<id>` | Get a specific customer |
| PUT | `/customers/<id>` | Update a customer |
| DELETE | `/customers/<id>` | Delete a customer |

**Example Request (POST `/customers/`):**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "555-1234"
}
```

### Mechanics (`/mechanics`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mechanics/` | Create a new mechanic |
| GET | `/mechanics/` | Get all mechanics |
| GET | `/mechanics/<id>` | Get a specific mechanic |
| PUT | `/mechanics/<id>` | Update a mechanic |
| DELETE | `/mechanics/<id>` | Delete a mechanic |

**Example Request (POST `/mechanics/`):**
```json
{
  "name": "Mike Mechanic",
  "email": "mike@shop.com",
  "address": "123 Main Street",
  "phone": "555-5678",
  "salary": 50000.00
}
```

### Service Tickets (`/service-tickets`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/service-tickets/` | Create a new service ticket |
| GET | `/service-tickets/` | Get all service tickets (includes assigned mechanics and customer) |
| GET | `/service-tickets/<id>` | Get a specific service ticket |
| PUT | `/service-tickets/<id>` | Update a service ticket |
| DELETE | `/service-tickets/<id>` | Delete a service ticket |
| PUT | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a service ticket |
| PUT | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a service ticket |

**Example Request (POST `/service-tickets/`):**
```json
{
  "vin": "1HGBH41JXMN109186",
  "service_date": "2025-12-14",
  "service_description": "Oil change and tire rotation",
  "customer_id": 1
}
```

**Example Response (GET `/service-tickets/`):**
```json
[
  {
    "id": 1,
    "vin": "1HGBH41JXMN109186",
    "service_date": "2025-12-14",
    "service_description": "Oil change and tire rotation",
    "customer_id": 1,
    "customer": {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "555-1234"
    },
    "mechanics": [
      {
        "id": 1,
        "name": "Mike Mechanic",
        "email": "mike@shop.com",
        "address": "123 Main Street",
        "phone": "555-5678",
        "salary": 50000.00
      }
    ]
  }
]
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful GET, PUT requests
- `201 Created`: Successful POST request
- `400 Bad Request`: Validation errors or invalid data
- `404 Not Found`: Resource not found

**Error Response Format:**
```json
{
  "error": "Error message description"
}
```

## Testing with Postman

1. Import the provided Postman collection
2. Set the base URL to `http://localhost:5000`
3. Test endpoints in the following order:
   - Create customers
   - Create mechanics
   - Create service tickets
   - Assign mechanics to service tickets
   - Retrieve all data to verify relationships
