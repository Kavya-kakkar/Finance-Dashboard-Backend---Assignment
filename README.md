# Finance Dashboard API

This is a backend system for a Finance Dashboard built with FastAPI, SQLite, SQLAlchemy, and Pydantic. It features strict Role-Based Access Control (RBAC) separating `Viewer`, `Analyst`, and `Admin` permissions.

## Tech Stack
* Language: Python 3
* Framework: FastAPI
* Database: SQLite (SQLAlchemy ORM)
* Validation: Pydantic

## Getting Started

### 1. Create a Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
Run the following command to install the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Initialize the Database
This script will automatically create the database schema (`finance.db`) and seed an initial default Admin user.
```bash
python init_db.py
```
*Initial Admin Credentials:*
* **Email:** `admin@finance.com`
* **Password:** `adminpassword`

### 4. Run the Application
Start the uvicorn development server:
```bash
uvicorn main:app --reload
```

## API Documentation
Once the server is running, you can explore, test, and view the automatically generated Swagger API documentation at:
* **Interactive Docs (Swagger UI):** http://127.0.0.1:8000/docs
* **Alternative Docs (ReDoc):** http://127.0.0.1:8000/redoc
*  **Live URL : **https://finance-dashboard-api-h66a.onrender.com/docs**

## App Structure
* `core/`: Application settings, database connection, JWT authorization, and role dependency logic.
* `models/`: SQLAlchemy ORM models (`User`, `Record`).
* `schemas/`: Pydantic models for request validation and response mapping.
* `services/`: Business logic implementations separating data manipulation from HTTP handling.
* `routes/`: FastAPI endpoints. Routing layers keeping endpoints clean.

## Features implemented:
* **User Management:** Create, update, view users, strict RBAC implemented using FastAPI Dependencies.
* **Financial Records:** Full CRUD for tracking expenses and income, with filtering.
* **Dashboard Summary:** Aggregated analytics providing net balance, category totals, and recent transaction history.
* **Auth:** Secure JWT-based authentication via OAuth2 `password` flow.
