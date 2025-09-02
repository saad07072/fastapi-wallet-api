import asyncio
import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import User

@pytest.fixture(autouse=True, scope="module")
def setup_db():
    # Fresh tables for tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_user_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # create a user
        resp = await ac.post("/users", json={"name":"Alice","email":"alice@example.com","phone":"+91-7000000000"})
        assert resp.status_code == status.HTTP_201_CREATED, resp.text
        user = resp.json()
        uid = user["id"]

        # list users shows balance 0
        resp = await ac.get("/users")
        assert resp.status_code == 200
        assert resp.json()[0]["balance"] == 0

        # credit 150
        resp = await ac.post(f"/wallets/{uid}/update", json={"amount":150.0, "description":"Top-up"})
        assert resp.status_code == 200
        tx1 = resp.json()
        assert tx1["amount"] == 150.0

        # debit 50
        resp = await ac.post(f"/wallets/{uid}/update", json={"amount":-50.0, "description":"Purchase"})
        assert resp.status_code == 200

        # check transactions
        resp = await ac.get(f"/wallets/{uid}/transactions")
        assert resp.status_code == 200
        txs = resp.json()
        assert len(txs) == 2

        # ensure balance shows 100 on list
        resp = await ac.get("/users")
        assert resp.status_code == 200
        users = resp.json()
        assert users[0]["balance"] == 100.0
