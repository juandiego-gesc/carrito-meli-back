# Back-end App Buses
## Technologies
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- Docker
- JWT
- MySQL

## Requirements
- Python 3.9

## Installation
To install the requirements in a venv, you can run the following commands:
```bash
python3 -m venv venv 
source venv/bin/activate # Activate the venv
pip install -r requirements.txt
```
Remember that it is only necessary to run the first command once.

After that, you'll need to create a .env file with the following content:
```bash
DB_NAME=''
DB_USERNAME=''
DB_PASSWORD=''
DB_HOST=''

#Auth
SECRET_KEY = ''
ALGORITHM = ''
ACCESS_TOKEN_EXPIRE_MINUTES = (int)

```

## DB Set Up
### 1. MySQL Docker Container

You can run a MySQL container using Docker. Replace the placeholders with your actual values:

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

Once your database is up and running, run this command in your project root:

**Apply Migrations**

   This command runs all pending migrations and updates your database schema:

   ```bash
   alembic upgrade head
   ```

## Usage
Once you have installed the requirements, set up the database and activated the venv, you can run the app with the following command:
```bash
uvicorn src.main.app:app --reload
```