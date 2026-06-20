from fastapi import FastAPI
from app.routes.payments import router as payment_router

app = FastAPI(title="FinSafe Payment API")

app.include_router(payment_router)