import time
from fastapi.responses import JSONResponse
from app.types.types import PaymentRequest

def payment_processing(data: PaymentRequest):
    time.sleep(2)
    return {
        "message": f"Charged GHS {data.amount}",
        "status" : 200
        
    }
      