# FastAPI Wallet Service

A simple wallet service built with **FastAPI** + **SQLAlchemy** + **SQLite** that meets the assignment requirements:

- **List Users API** – Fetch all users (name, email, phone) along with their wallet balance.
- **Update Wallet API** – Add or deduct an amount for a user's wallet (creates a transaction and updates balance).
- **Fetch Transactions API** – Get all wallet transactions for a specific user by `user_id`.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs  
ReDoc: http://127.0.0.1:8000/redoc

> Default DB is SQLite at `wallet.db` in the project root. Tables auto-create on first run.

## API Overview

- `GET /users` → List users with `name, email, phone, balance`
- `POST /users` → Create a user (helper endpoint for testing)
- `POST /wallets/{user_id}/update` → Update wallet (credit or debit) with body: `{"amount": 100.0, "description": "Initial Top-up"}`
- `GET /wallets/{user_id}/transactions` → All transactions for a user

### Notes
- Positive amount ⇒ **credit**, Negative amount ⇒ **debit**.
- Every update creates a transaction row and updates the user's balance atomically.
- Basic validation (e.g., user must exist, balance cannot go below zero unless `allow_negative=True`).

## Running Tests

```bash
pytest -q
```

## Docker

```bash
docker build -t fastapi-wallet .
docker run -p 8000:8000 fastapi-wallet
```

## Deploy (Render example)

1. Push this repo to GitHub.
2. Create a new **Web Service** on Render: runtime **Docker**.
3. Set the start command (Dockerfile handles it).

## Project Structure

```
app/
  __init__.py
  main.py
  database.py
  models.py
  schemas.py
  crud.py
  routers/
    __init__.py
    users.py
    wallets.py
tests/
  test_api.py
wallet.db           # created at runtime
requirements.txt
Dockerfile
```

---

### Extra Credit Ideas Implemented
- Clean router separation, Pydantic schemas.
- Tests with `pytest` and `httpx` AsyncClient.
- Dockerfile for hosting.
