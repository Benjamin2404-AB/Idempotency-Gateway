Good — this is where your project goes from “working API” to “submission that stands out.”

I’ll give you a **clean architecture + a ready-to-paste README** you can directly use or tweak.

---

# 🧱 1. Architecture (what you should include)

You want a **simple flow diagram + explanation**.

## 📌 System Architecture (text version)

```
Client
  │
  │  POST /process-payment (Idempotency-Key)
  ▼
FastAPI Router (API Layer)
  │
  │  1. Validate request
  │  2. Extract Idempotency-Key
  ▼
Concurrency Control Layer
  │
  │  Per-key Lock (in_flight_locks)
  │  → prevents race conditions
  ▼
Idempotency Layer
  │
  ├── Key exists?
  │      ├── Yes → compare payload
  │      │         ├── same → return cached response
  │      │         └── different → 422 error
  │      └── No → continue processing
  ▼
Payment Service Layer
  │
  │  Simulates external payment gateway (2s delay)
  ▼
Transaction Store (in-memory dict)
  │
  │  Saves:
  │   - payment
  │   - response
  │   - timestamp
  │   - status
  ▼
Response returned to client
```

---

## 📌 Audit Endpoint Flow

```
Client → GET /transactions/{key}
            │
            ▼
      Transaction Store
            │
            ▼
   Returns audit record
```

---

# 🧾 2. FULL README (copy this)

You can paste this directly into your repository.

---

# 💳 Idempotency Layer for Payment Processing API

## 📌 Overview

This project implements a **payment processing API with an idempotency layer** to prevent duplicate transactions caused by network retries.

It ensures that each payment request is processed **exactly once**, even if the client retries multiple times due to timeouts or failures.

---

# 🚨 Problem Statement

Payment systems often face a critical issue:

> Clients retry requests due to network delays, causing duplicate charges.

This system solves that by introducing:

* Idempotency-Key validation
* Request deduplication
* Race condition protection
* Transaction audit logging

---

# 🏗️ Architecture

The system is built using a layered architecture:

### 1. API Layer (FastAPI)

Handles HTTP requests and input validation.

### 2. Concurrency Control Layer

Uses **per-Idempotency-Key locks** to prevent race conditions.

### 3. Idempotency Layer

Ensures:

* First request is processed
* Duplicate requests return cached result
* Conflicting payloads are rejected

### 4. Service Layer

Simulates payment processing (2-second delay).

### 5. Storage Layer (In-Memory)

Stores transaction data for:

* replay protection
* audit history

### 6. Audit Layer

Exposes transaction history via query endpoint.

---

# 🔐 Key Features

## ✅ Idempotency Protection

Prevents duplicate payment processing using `Idempotency-Key`.

## ✅ Race Condition Safety

Uses **thread locks per key** to ensure atomic execution.

## ✅ Payload Integrity Check

Rejects requests with same key but different payload.

## ✅ Transaction Audit Trail

Stores full transaction history with:

* timestamp
* status
* response
* payment details

## ✅ Cache Hit Optimization

Returns cached response instantly for duplicate requests.

---

# 📡 API Endpoints

---

## 🔹 POST /process-payment

### Headers

```
Idempotency-Key: unique-key
```

### Body

```json
{
  "amount": 100,
  "currency": "GHS"
}
```

---

### Response (First Request)

```json
{
  "message": "Charged 100 GHS"
}
```

---

### Response (Duplicate Request)

```json
{
  "message": "Charged 100 GHS"
}
```

Header:

```
X-Cache-Hit: true
```

---

### Response (Different Payload, Same Key)

```json
{
  "message": "Idempotency key already used for a different request body"
}
```

Status:

```
422 Unprocessable Entity
```

---

## 🔹 GET /transactions/{key}

### Description

Returns stored transaction for auditing.

### Response

```json
{
  "idempotency_key": "abc123",
  "amount": 100,
  "currency": "GHS",
  "status": "completed",
  "timestamp": "2026-06-20T10:30:00Z",
  "response": {
    "message": "Charged 100 GHS"
  }
}
```

---

# 🧠 Design Decisions

## 1. In-Memory Store

Used a Python dictionary for simplicity and speed.

## 2. Per-Key Locking

Ensures only one request per Idempotency-Key is processed at a time.

## 3. Transaction Model

Created a structured `Transaction` object to support auditing and traceability.

## 4. Simulated Payment Delay

Used `sleep(2)` to mimic external payment gateway latency.

---

# 💡 Developer Choice Feature

## 📊 Transaction Audit API

An additional endpoint was added:

```
GET /transactions/{key}
```

### Why it matters:

* Enables auditability of payments
* Helps debugging failed transactions
* Provides transparency for financial operations
* Turns system into a lightweight ledger

---

# ⚠️ Limitations

* Uses in-memory storage (not persistent)
* Not distributed-safe (locks are per-process only)
* No TTL for idempotency keys

---



# 🧪 How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

# 🧠 Summary

This system guarantees:

> Each payment is processed exactly once, even under retries or concurrent requests.

---


