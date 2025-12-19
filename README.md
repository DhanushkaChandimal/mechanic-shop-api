# Mechanic Shop API

A RESTful API for managing a mechanic shop's operations, including customers, mechanics, service tickets, and inventory items. Built with Flask, SQLAlchemy, and Marshmallow using the Application Factory Pattern.

## Features

- **Customer Management**: Create, read, and delete customer records with JWT authentication
- **Mechanic Management**: Full CRUD operations for mechanic profiles
- **Service Ticket Management**: Track service requests and repairs
- **Item Management**: Manage parts and inventory items
- **Mechanic Assignment**: Assign and remove mechanics to/from service tickets
- **Parts Integration**: Add items/parts to service tickets with quantity tracking
- **JWT Authentication**: Secure customer-specific endpoints with token-based authentication
- **Rate Limiting**: Protect API endpoints from abuse
- **Caching**: Improve performance with response caching
- **Many-to-Many Relationships**: Multiple mechanics can work on multiple service tickets
- **Data Validation**: Marshmallow schemas for request/response validation
- **Blueprint Architecture**: Modular, scalable application structure

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Marshmallow**: Object serialization/deserialization
- **Flask-SQLAlchemy**: Flask integration with SQLAlchemy
- **Flask-Marshmallow**: Flask integration with Marshmallow
- **Flask-Limiter**: Rate limiting
- **Flask-Caching**: Response caching
- **PyJWT**: JSON Web Token authentication
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
│       ├── items/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       └── service_ticket/
│           ├── __init__.py
│           ├── routes.py
│           └── schemas.py
│   └── utils/
│       └── util.py
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
| POST | `/customers/` | Create a new customer (includes JWT token in response) |
| POST | `/customers/login` | Login and receive JWT token |
| GET | `/customers/` | Get all customers |
| GET | `/customers/<id>` | Get a specific customer |
| DELETE | `/customers/<id>` | Delete a customer |

**Example Request (POST `/customers/`):**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "555-1234",
  "password": "securepassword123"
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

### Items (`/items`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/items/` | Create a new item/part |
| GET | `/items/` | Get all items |
| GET | `/items/<id>` | Get a specific item |
| PUT | `/items/<id>` | Update an item |
| DELETE | `/items/<id>` | Delete an item |

**Example Request (POST `/items/`):**
```json
{
  "name": "Oil Filter",
  "price": 25.99
}
```

### Service Tickets (`/service-tickets`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/service-tickets/` | Create a new service ticket (rate limited: 30/hour) |
| GET | `/service-tickets/` | Get all service tickets with mechanics and items |
| GET | `/service-tickets/<id>` | Get a specific service ticket |
| GET | `/service-tickets/my-tickets` | Get tickets for authenticated customer (requires JWT) |
| PUT | `/service-tickets/<ticket_id>/edit` | Add/remove mechanics from a ticket |
| PUT | `/service-tickets/add-part/<item_id>/to-ticket/<ticket_id>` | Add an item to a ticket (increments quantity if already exists) |
| DELETE | `/service-tickets/<id>` | Delete a service ticket (rate limited: 2/hour) |

**Example Request (POST `/service-tickets/`):**
```json
{
  "vin": "1HGBH41JXMN109186",
  "service_date": "2025-12-14",
  "service_description": "Oil change and tire rotation",
  "customer_id": 1
}
```

**Example Request (PUT `/service-tickets/<ticket_id>/edit`):**
```json
{
  "add_mechanic_ids": [1, 2],
  "remove_mechanic_ids": []
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
    "mechanics": [
      {
        "id": 1,
        "name": "Mike Mechanic",
        "phone": "555-5678"
      }
    ],
    "items": [
      {
        "id": 1,
        "name": "Oil Filter",
        "price": 25.99,
        "quantity": 2
      }
    ]
  }
]
```

## Authentication

Protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

**Protected Endpoints:**
- `GET /service-tickets/my-tickets`: Get tickets for the authenticated customer

**Getting a Token:**
1. Create a customer account: `POST /customers/`
2. Login: `POST /customers/login` with email and password
3. Use the returned token in the Authorization header

## Rate Limiting

Some endpoints have rate limits to prevent abuse:
- `POST /service-tickets/`: 30 requests per hour
- `DELETE /service-tickets/<id>`: 2 requests per hour

## Caching

The `GET /service-tickets/` endpoint is cached for 60 seconds to improve performance.

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful GET, PUT requests
- `201 Created`: Successful POST request
- `400 Bad Request`: Validation errors or invalid data
- `401 Unauthorized`: Missing or invalid authentication token
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded

**Error Response Format:**
```json
{
  "error": "Error message description"
}
```

## Testing with Postman

1. Import the provided Postman collection (`Mechanic Shop With Data.postman_collection.json`)
2. Set the base URL to `http://localhost:5000`
3. Test endpoints in the following order:
   - Create customers
   - Login with customer credentials (save the JWT token)
   - Create mechanics
   - Create items/parts
   - Create service tickets
   - Add mechanics to service tickets
   - Add parts to service tickets
   - Retrieve all data to verify relationships
   - Test authenticated endpoint with JWT token
