# Logistics Microservice (Backend)

This is the backend service for the Logistics Application, built with **FastAPI**, **PostgreSQL**, and **Docker**. It handles inventory management, order processing, and strict concurrency control.

## Prerequisites
- **Docker Desktop** (Must be installed and running)
- **Git**

## Quick Start Commands

### 1. Start the Server
Run this command to build and start the database and API containers.
```bash
docker-compose up --build
```

The API will start on http://localhost:3000 check docker-compose.yml.

### 2. Apply Database Migrations
Once the server is running (in a new terminal), set up the database tables:
```bash
docker-compose exec web alembic upgrade head
```

### 3. Run Tests
To verify the application logic and locking mechanisms:
```bash
docker-compose exec web pytest
```

### 4. Stop the Server
To stop and remove the containers:
```bash
docker-compose down
```

### API Documentation
Once running, you can access the interactive API docs here:

Swagger UI: http://localhost:3000/docs

### Technical Design
Concurrency Handling: To prevent race conditions (overselling stock), this project uses Pessimistic Locking (SELECT ... FOR UPDATE) in SQLAlchemy. This ensures that when an order is being processed, the specific product row is locked until the transaction commits, preventing other parallel requests from modifying the stock simultaneously.


### Frontend Repo Link

Repo of logistics-frontend: https://github.com/manojitht/logistics-frontend

