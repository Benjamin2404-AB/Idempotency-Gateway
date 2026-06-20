import datetime
from threading import Lock

from fastapi import APIRouter, Header, HTTPException ,Response
from fastapi.responses import JSONResponse

from app.services.payment_service import payment_processing
from app.store import trans_db,in_flight_locks
from app.types.types import Transaction, TransactionStatus , PaymentRequest

router = APIRouter()


@router.post("/process-payment")
def process_payment(
    payment: PaymentRequest,
    response:Response,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key")
):
    

    # Check if Idempotency Key actually exists in the Header of request being sent 
    if not idempotency_key:
        raise HTTPException(
                status_code=400,
                detail="Idempotency-Key header is required"
        )
    lock = in_flight_locks.setdefault(idempotency_key, Lock())
    with lock:

        # Check if idempotency-key exists
        if idempotency_key in trans_db:
            cached_data = trans_db[idempotency_key]

            # First check if payload is different status 422 Unprocessable Entity
            if cached_data.payment.model_dump() != payment.dict():
                return JSONResponse(
            status_code=422,
            content={
                "message": "Idempotency key already used for a different request body"
            })

            #payload is the same , return same response , cache hit true
            response.headers["X-Cache-Hit"] = "true"
            return JSONResponse(content=cached_data.response)



        res = payment_processing(payment)
        transaction = Transaction(
        i_key=idempotency_key,
        payment=payment.dict(),
        response=res,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        status=TransactionStatus.completed

        )

        trans_db[idempotency_key] = transaction



        return res
    



@router.get("/transactions/{key}")
def get_transaction(key: str):
    if key not in trans_db:
        raise HTTPException(status_code=404, detail="Transaction not found")

    tx = trans_db[key]

    return {
        "idempotency_key": tx.i_key,
        "amount": tx.payment.amount,
        "currency": tx.payment.currency,
        "status": tx.status.value,
        "timestamp": tx.timestamp,
        "response": tx.response
    }