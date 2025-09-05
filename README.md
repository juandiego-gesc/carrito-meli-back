# Carrito Meli - Backend API

A robust e-commerce cart management system API built with FastAPI, providing secure authentication and product management capabilities.

## Project Overview

The Carrito Meli backend is a RESTful API that handles shopping cart functionality for an e-commerce platform. It manages user authentication, product catalog, and shopping cart operations through a clean, layered architecture:

- **API Layer**: FastAPI routes and controllers
- **Logic Layer**: Business logic implementation
- **Data Layer**: Database models and operations

## Technologies

- **Python**: Core programming language
- **FastAPI**: Web framework for building APIs
- **Pydantic**: Data validation and settings management
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **Docker**: Containerization
- **JWT**: Authentication mechanism
- **MySQL**: Database system

## Architecture

The application follows a three-tier architecture:
- **Controllers**: Handle HTTP requests and responses (`controller/` directory)
- **Logic**: Contain business rules and validation (`logic/` directory)
- **Models**: Database models and data access (`bd/models/` directory)

## API Endpoints Documentation

### Authentication
- **POST /auth/token**: Get JWT token
  - Request: `{ "username": "string", "password": "string" }`
  - Response: `{ "access_token": "string", "token_type": "bearer" }`

### User Management
- **POST /users/create**: Create new user
  - Request: User details (username, password, etc.)
  - Response: Created user details

- **PUT /users/update**: Update user information (authenticated)
  - Request: Updated user details
  - Response: Updated user information

- **DELETE /users/delete/{user_id}**: Delete user (authenticated)
  - Response: Deletion confirmation

- **GET /users/get/all**: List all users
  - Response: Array of user details

- **GET /users/get/{user_id}**: Get user by ID
  - Response: User details

- **GET /users/get/username/{username}**: Get user by username
  - Response: User details

### Product Management
- **POST /products/create**: Create new product
  - Request: Product details (name, price, etc.)
  - Response: Created product details

- **PUT /products/update**: Update product information
  - Request: Updated product details
  - Response: Updated product information

- **DELETE /products/delete/{product_id}**: Delete product
  - Query Param: `mode` ("soft" or "hard")
  - Response: Deletion confirmation

- **GET /products/all**: List all products
  - Response: Array of product details

- **GET /products/{product_id}**: Get product by ID
  - Response: Product details

### Cart Management
- **POST /cart/create**: Add item to cart (authenticated)
  - Request: Cart item details (product_id, quantity, etc.)
  - Response: Created cart item

- **PUT /cart/update**: Update cart item (authenticated)
  - Request: Updated cart item details
  - Response: Updated cart item

- **DELETE /cart/delete/{cart_item_id}**: Delete cart item (authenticated)
  - Query Param: `mode` ("soft" or "hard")
  - Response: Deletion confirmation

- **GET /cart/**: Get user's cart items (authenticated)
  - Response: Array of cart items

## Authentication Flow

The API uses JWT (JSON Web Token) for authentication:

1. User submits credentials to `/auth/token` or `/users/login`
2. Server validates credentials and returns JWT token
3. Client includes token in Authorization header for protected routes
4. Server validates token on each protected request

The token contains the user ID and username, and expires after the configured time (set in .env file).

## Requirements

- Python 3.9+
- MySQL database

## Installation

To install the requirements in a virtual environment, run:

```bash
python3 -m venv venv 
source venv/bin/activate # Activate the venv
pip install -r requirements.txt
```

After that, create a `.env` file with the following content:

```bash
DB_NAME='your_database_name'
DB_USERNAME='your_database_username'
DB_PASSWORD='your_database_password'
DB_HOST='localhost'

# Auth
SECRET_KEY='your_secret_key_here'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## DB Set Up

### 1. MySQL Docker Container

You can run a MySQL container using Docker:

```bash
docker run --name mysql-container \
  -e MYSQL_ROOT_PASSWORD=your_root_password \
  -e MYSQL_DATABASE=your_db_name \
  -e MYSQL_USER=your_db_user \
  -e MYSQL_PASSWORD=your_db_password \
  -p 3306:3306 \
  -d mysql:8
```

### 2. Alembic Migrations

Once your database is running, apply migrations:

```bash
alembic upgrade head
```

## Usage

Once you have installed the requirements, set up the database and activated the venv, run:

```bash
uvicorn src.main.app:app --reload
```

The API will be available at http://127.0.0.1:8000

Interactive API documentation is available at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Logs

The application logs are stored in the `logs/` directory. The current log file is `app.log`, and dated logs are kept for historical purposes.

To check logs:

```bash
tail -f logs/app.log
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure your MySQL container is running: `docker ps`
   - Verify .env configuration matches your database settings

2. **Authentication Issues**
   - Check that SECRET_KEY and ALGORITHM are properly set in .env
   - Ensure token is correctly included in Authorization header

3. **Migration Errors**
   - Run `alembic current` to check current migration state
   - Try `alembic stamp head` followed by `alembic upgrade head` to reset migrations

## Deployment

The project includes a Dockerfile for containerized deployment:

```bash
docker build -t carrito-meli-api .
docker run -p 8000:8000 carrito-meli-api
```

