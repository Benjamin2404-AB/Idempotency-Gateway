import datetime
from enum import Enum

from pydantic import BaseModel


class TransactionStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class PaymentRequest(BaseModel):
    """_summary_

    Args:
        amount (_int_):  _this refers to the payment amount_
        currency (_string_) : _this is the currency in which the payment is being carried out_
        BaseModel (_type_): _attributes are amount and currency_
    """
    amount : int
    currency : str
    
    
class Transaction(BaseModel):
    """_summary_

    Args:
        i_key (_str_): _idempotency key to prevent duplicate transactions_
        payment (_PaymentRequest_): _ this contains the amount and currency of transaction _
        timestamp (_datetime_): _timestamp of transaction_
        response (_dict_): _this serves as a response for the transaction returns a staus of 200 and a message_
        
    """
    i_key : str
    payment : PaymentRequest
    timestamp: datetime.datetime
    response: dict | None = None
    status: TransactionStatus
    