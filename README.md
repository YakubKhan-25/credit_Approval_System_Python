# credit_Approval_System_Python

A Django-based Credit Approval System for registering customers, checking loan eligibility, and managing loans. The backend uses PostgreSQL and is fully containerized with Docker for easy setup.

## What does this project do?

- Registers customers and calculates their approved credit limit based on income.
- Checks loan eligibility using customer credit score and income.
- Creates and manages loans for customers.
- Provides REST API endpoints for all operations.

## How to Run

### 1. Clone the Repository

### Enter into backend

cd credit_Approval_System_Python/backend

### 2. Build and Start with Docker Compose

```bash
docker-compose up -d --build
```

- Django app: http://localhost:8000
- PostgreSQL: localhost:5432

### 3. API Endpoints

| Endpoint                     | Method | Description                     |
| ---------------------------- | ------ | ------------------------------- |
| `/register/`                 | POST   | Register a new customer         |
| `/check-eligibility/`        | POST   | Check loan eligibility          |
| `/create-loan/`              | POST   | Create a new loan               |
| `/view-loan/<loan_id>/`      | GET    | View details of a specific loan |
| `/view-loans/<customer_id>/` | GET    | View all loans for a customer   |

### 4. Enter the Database Container to check the stored (actual) data.

```bash
docker ps
### Find the db container name, e.g., credit_approval_system_db_1
docker exec -it <your_db_container_name> bash
```

### 5. Access PostgreSQL

```bash
psql -U <your_db_user> -d <your_db_name>
```

#### Useful PostgreSQL Commands

- List tables: `\dt`
- Table schema: `\d <table_name>`
- Query: `SELECT * FROM core_customer;`
- Exit: `\q`

## Environment Variables (see docker-compose.yml)

- `DB_HOST=<your_db_host>`
- `DB_NAME=<your_db_name>`
- `DB_USER=<your_db_user>`
- `DB_PASS=<your_db_pass>`

## Manual Development (Optional)

```bash
cd backend/app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## Backend

Go to the `backend` directory and run the project with a single Docker command:

```bash

docker-compose up -d


Replace all <your\_...> placeholders with your actual values as needed.
