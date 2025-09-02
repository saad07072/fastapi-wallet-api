from fastapi import FastAPI
from .database import Base, engine
from .routers import users, wallets

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Wallet Service API",
    version="1.0.0",
    description="Simple wallet APIs (Users, Wallet Update, Transactions)"
)

app.include_router(users.router)
app.include_router(wallets.router)

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok"}
