from app.types.types import Transaction

from threading import Lock

in_flight_locks: dict[str, Lock] = {}


trans_db: dict[str, Transaction] = {}
